from django.contrib import admin

from tanaman.models import Tanaman

# Register your models here.
@admin.register(Tanaman)
class TanamanAdmin(admin.ModelAdmin):
    fields = ('daerah','nama_tanaman','jenis_tanaman')
    list_display= ('id','daerah','nama_tanaman','jenis_tanaman')