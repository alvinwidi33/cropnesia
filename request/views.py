from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from hasil_pertanian.models import HasilPertanian
from request.models import Request
from request.serializers import *
from django.shortcuts import get_object_or_404

from tanaman.models import Tanaman

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

    # Update the request status to 'Accepted'
    serializer = RequestSerializerPost(permintaan, data={'status_request': 'Accepted'}, partial=True)
    if serializer.is_valid():
        serializer.save()

        # Update the quantities in HasilPertanian for both Pemerintah A and B
        hasil_pertanian_a = permintaan.id_hasil_pertanian
        pemerintah_b = permintaan.id_pemerintah_request

        # Get daerah of Pemerintah A and B
        daerah_a = hasil_pertanian_a.id_tanaman.daerah.user.daerah
        daerah_b = pemerintah_b.user.daerah

        # Check if Pemerintah B has the crop
        try:
            hasil_pertanian_b = HasilPertanian.objects.get(
                id_tanaman=hasil_pertanian_a.id_tanaman,
                id_tanaman__daerah__user__daerah=daerah_b
            )
            hasil_pertanian_b.kuantitas += hasil_pertanian_a.kuantitas
            hasil_pertanian_b.save()
        except HasilPertanian.DoesNotExist:
            # If Pemerintah B doesn't have the crop, create a new entry
            HasilPertanian.objects.create(
                id_tanaman=hasil_pertanian_a.id_tanaman,
                kuantitas=hasil_pertanian_a.kuantitas,
                harga_hasil_pertanian=hasil_pertanian_a.harga_hasil_pertanian,
                status_panen=hasil_pertanian_a.status_panen,
                daerah=daerah_b  # Set daerah to Pemerintah B's daerah
            )

        # Subtract the quantity from Pemerintah A
        hasil_pertanian_a.kuantitas -= permintaan.id_hasil_pertanian.kuantitas
        hasil_pertanian_a.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)