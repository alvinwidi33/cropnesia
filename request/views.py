from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from request.models import Request
from request.serializers import *

@api_view(['GET'])
def get_list_request(request,id_pemerintah_request):
    pemerintah_request = Request.objects.filter(id_pemerintah_request__pemerintah_id=id_pemerintah_request)
    serializer = PemerintahSerializerGet(pemerintah_request, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_request(request):
    serializer = RequestSerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH']) 
def verify_request(request, id):
    try:
        permintaan = Request.objects.get(id=id)
    except Request.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RequestSerializerPost(permintaan, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)