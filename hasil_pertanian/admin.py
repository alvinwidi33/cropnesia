from django.contrib import admin
from .models import HasilPertanian
# Register your models here.
@admin.register(HasilPertanian)
class HasilPertanianAdmin(admin.ModelAdmin):
    fields = ("id_tanaman","kuantitas","harga_hasil_pertanian","status_panen","datetime_panen")
    list_display = ("id","id_tanaman","kuantitas","harga_hasil_pertanian","status_panen","datetime_panen")