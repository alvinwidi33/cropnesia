from django.contrib import admin

from negosiasi_request.models import NegosiasiRequest

# Register your models here.
@admin.register(NegosiasiRequest)
class NegosiasiRequestAdmin(admin.ModelAdmin):
    fields = ("id_request","message")
    list_display = ("id","id_request","message","datetime_chat")