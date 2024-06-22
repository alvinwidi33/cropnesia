from rest_framework import serializers
from .models import Request
from user.serializers import PemerintahSerializerGet
from hasil_pertanian.serializers import HasilPertanianGet
class RequestSerializerGet(serializers.ModelSerializer):
    id_hasil_pertanian = HasilPertanianGet()
    id_pemerintah_request = PemerintahSerializerGet()
    class Meta:
        model = Request
        fields = ("id","id_pemerintah_request","id_hasil_pertanian","status_request","datetime_request","jumlah_diminta")

class RequestSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ("id","id_pemerintah_request","id_hasil_pertanian","status_request","datetime_request","jumlah_diminta")