from django.contrib import admin
from .models import Request
# Register your models here.
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    fields = ("id_pemerintah_request","id_hasil_pertanian","status_request")
    list_display = ("id","id_pemerintah_request","id_hasil_pertanian","status_request","datetime_request")