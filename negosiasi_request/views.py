from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from negosiasi_request.models import NegosiasiRequest
from negosiasi_request.serializers import *

# Create your views here.
@api_view(['POST'])
def add_negosiasi_request(request):
    serializer = NegosiasiRequestPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_list_negosiasi_request(request, id_request):
    negosiasi_request = NegosiasiRequest.objects.filter(is_request__id = id_request)
    serializer = NegosiasiRequestGet(negosiasi_request, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)