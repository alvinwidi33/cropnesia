import os
import random
import string
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.permission import is_admin  # Ensure this is defined and correctly imported
from .models import User, Pemerintah, Petani, Admin
from .serializers import (
    UserSerializer, PemerintahSerializerPost, PemerintahSerializerGet,
    PetaniSerializerPost, PetaniSerializerGet, AdminSerializerPost, AdminSerializerGet
)
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(pk=token.user_id)
        user_serializer = UserSerializer(user, many=False)
        return Response({'token': token.key, 'user': user_serializer.data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([is_admin])
def add_user(request):
    dataUser = request.data
    email = dataUser['email']
    username = dataUser['username']
    name = dataUser['name']

    # Check if email or username already exists
    if User.objects.filter(Q(email=email) | Q(username=username)).exists():
        return Response({'error': 'Email or username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed(os.urandom(1024))
    password = ''.join(random.choice(chars) for i in range(length))
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(password)
        user.save()
        
        role = user.role
        if role == 'Pemerintah':
            pemerintah_data = {'user': user.user_id}
            pemerintah_serializer = PemerintahSerializerPost(data=pemerintah_data)
            if pemerintah_serializer.is_valid():
                pemerintah_serializer.save()
            else:
                user.delete() 
                return Response(pemerintah_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif role == 'Petani':
            petani_data = {'user': user.user_id}
            petani_serializer = PetaniSerializerPost(data=petani_data)
            if petani_serializer.is_valid():
                petani_serializer.save()
            else:
                user.delete()  
                return Response(petani_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif role == 'Admin':
            admin_data = {'user': user.user_id}
            admin_serializer = AdminSerializerPost(data=admin_data)
            if admin_serializer.is_valid():
                admin_serializer.save()
            else:
                user.delete()
                return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Email user initial login information
        views_dir = os.path.dirname(__file__)
        
        html_template_path = os.path.join(views_dir, 'add_user_email.html')
        
        with open(html_template_path, 'r') as file:
            html_message = file.read()
        
        html_message = html_message.replace('{{ name }}', name)
        html_message = html_message.replace('{{ username }}', username)
        html_message = html_message.replace('{{ email }}', email)
        html_message = html_message.replace('{{ password }}', password)
        
        subject = 'Informasi Akun User Cropnesia'
        from_email = 'Cropnesia@gmail.com'
        to_email = [email]
        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
        except Exception as e:
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([is_admin])
def update_user_role(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    new_role = request.data.get('role')

    if not new_role:
        return Response({"error": "Role field is required"}, status=status.HTTP_400_BAD_REQUEST)

    if new_role not in dict(User.ROLES).keys():
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    user.role = new_role
    user.save()

    existing_role = None
    if new_role == 'Pemerintah':
        existing_role = Pemerintah.objects.filter(user=user).first()
    elif new_role == 'Petani':
        existing_role = Petani.objects.filter(user=user).first()
    elif new_role == 'Admin':
        existing_role = Admin.objects.filter(user=user).first()

    if existing_role:
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)

    role_data = {'user': user.user_id}
    serializer = None
    if new_role == 'Pemerintah':
        serializer = PemerintahSerializerPost(data=role_data)
    elif new_role == 'Petani':
        serializer = PetaniSerializerPost(data=role_data)
    elif new_role == 'Admin':
        serializer = AdminSerializerPost(data=role_data)

    if serializer and serializer.is_valid():
        serializer.save()
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to create new role object"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    logout(request)
    return JsonResponse({"message": "Logout successful"})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([is_admin])
def get_list_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_token_by_user(request, token_key):
    try:
        token = Token.objects.get(key=token_key)
        user = token.user

        if user.role == "Pemerintah":
            pemerintah = Pemerintah.objects.get(user=user)
            serializer = PemerintahSerializerGet(pemerintah)
        elif user.role == "Petani":
            petani = Petani.objects.get(user=user)
            serializer = PetaniSerializerGet(petani)
        elif user.role == "Admin":
            admin = Admin.objects.get(user=user)
            serializer = AdminSerializerGet(admin)
        else:
            serializer = UserSerializer(user)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([is_admin])
def get_list_petani_daerah(request, daerah):
    petanis = Petani.objects.filter(user__daerah=daerah)
    serializer = PetaniSerializerGet(petanis, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)