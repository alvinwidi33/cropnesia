from rest_framework import serializers
from user.serializers import PemerintahSerializerGet
from .models import Tanaman

class TanamanSerializerGet(serializers.Serializer):
    daerah = PemerintahSerializerGet()
    class Meta:
        model = Tanaman
        fields = ('id','daerah','nama_tanaman','jenis_tanaman')

class TanamanSerializerPost(serializers.Serializer):
    class Meta:
        model = Tanaman
        fields = ('id','daerah','nama_tanaman','jenis_tanaman')