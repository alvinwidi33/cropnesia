from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from hasil_pertanian.models import HasilPertanian
from hasil_pertanian.serializers import *

@api_view(['POST'])
def add_hasil_pertanian(request):
    serializer = HasilPertanianPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_hasil_pertanian(request, id):
    try:
        hasil_pertanian = HasilPertanian.objects.get(id=id)
    except HasilPertanian.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = HasilPertanianPost(hasil_pertanian, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_list_hasil_pertanian(request):
    hasil_pertanian = HasilPertanian.objects.all()
    serializer = HasilPertanianGet(hasil_pertanian, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_list_hasil_pertanian_daerah(request, daerah):
    hasil_pertanian = HasilPertanian.objects.filter(id_tanaman__daerah__user__daerah = daerah)
    serializer = HasilPertanianGet(hasil_pertanian, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)