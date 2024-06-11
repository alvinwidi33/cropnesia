from rest_framework import serializers
from .models import HasilPertanian
from tanaman.serializers import TanamanSerializerGet

class HasilPertanianGet(serializers.ModelSerializer):
    id_tanaman = TanamanSerializerGet()
    class Meta:
        model = HasilPertanian
        fields = ("id","id_tanaman","kuantitas","harga_hasil_pertanian","status_panen","datetime_panen")

class HasilPertanianPost(serializers.ModelSerializer):
    class Meta:
        model = HasilPertanian
        fields = ("id","id_tanaman","kuantitas","harga_hasil_pertanian","status_panen","datetime_panen")