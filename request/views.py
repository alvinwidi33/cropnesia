from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from hasil_pertanian.models import HasilPertanian
from request.models import Request
from request.serializers import RequestSerializerPost
from tanaman.models import Tanaman
from user.models import Pemerintah
from user.serializers import *

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

    serializer = RequestSerializerPost(permintaan, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        # If the request is accepted, transfer the padi
        if request.data.get('status_request') == 'Terima':
            id_pemerintah_A = permintaan.id_hasil_pertanian.id_tanaman.daerah.pemerintah_id
            id_pemerintah_B = permintaan.id_pemerintah_request.daerah.pemerintah_id

            try:
                # Pemerintah A
                hasil_pertanian_A = HasilPertanian.objects.get(id=permintaan.id_hasil_pertanian.id)
                hasil_pertanian_A.kuantitas -= permintaan.id_hasil_pertanian.kuantitas
                hasil_pertanian_A.save()

                # Pemerintah B
                tanaman_b, created = Tanaman.objects.get_or_create(
                    daerah_id=id_pemerintah_B,
                    nama_tanaman=hasil_pertanian_A.id_tanaman.nama_tanaman,
                    defaults={'jenis_tanaman': hasil_pertanian_A.id_tanaman.jenis_tanaman}
                )

                hasil_pertanian_B, created = HasilPertanian.objects.get_or_create(
                    id_tanaman=tanaman_b,
                    defaults={
                        'kuantitas': 0,
                        'harga_hasil_pertanian': hasil_pertanian_A.harga_hasil_pertanian,
                        'status_panen': hasil_pertanian_A.status_panen,
                        'datetime_panen': hasil_pertanian_A.datetime_panen,
                    }
                )

                hasil_pertanian_B.kuantitas += permintaan.id_hasil_pertanian.kuantitas
                hasil_pertanian_B.save()

            except HasilPertanian.DoesNotExist:
                return Response({"detail": "Pemerintah A does not have the requested padi."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)