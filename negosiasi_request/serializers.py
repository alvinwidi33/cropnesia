from rest_framework import serializers
from request.models import Request
from .models import NegosiasiRequest

class NegosiasiRequestGet(serializers.ModelSerializer):
    id_request = Request()
    class Meta:
        model = NegosiasiRequest
        fields = ("id","id_request","message","datetime_chat")

class NegosiasiRequestPost(serializers.ModelSerializer):
    class Meta:
        model = NegosiasiRequest
        fields = ("id","id_request","message","datetime_chat")