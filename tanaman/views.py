from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from tanaman.models import Tanaman
from tanaman.serializers import *

@api_view(['GET'])
def get_list_tanaman_daerah(request, daerah):
    tanamans = Tanaman.objects.filter(daerah__user__daerah = daerah)
    serializer = TanamanSerializerGet(tanamans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_tanaman(request):
    serializer = TanamanSerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)