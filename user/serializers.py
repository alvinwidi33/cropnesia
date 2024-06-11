from rest_framework import serializers
from .models import User,Admin,Pemerintah,Petani

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id",'username','name','role','daerah')

class PemerintahSerializerGet(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Pemerintah
        fields = ("pemerintah_id",'user')

class PemerintahSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Pemerintah
        fields = ("pemerintah_id",'user')

class PetaniSerializerGet(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Petani
        fields = ("petani_id",'user')

class PetaniSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Petani
        fields = ("petani_id",'user')

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ("admin_id",'user')