from django.db import models
from user.models import Pemerintah

class Tanaman(models.Model):
    JENIS =[
        ("Umbi-Umbian","Umbi-Umbian"),
        ("Biji-bijian","Biji-bijian"),
        ("Buah-buahan","Buah-buahan"),
        ("Rempah-rempah","Rempah-rempah"),
        ("Obat-obatan","Obat-obatan"),
        ("Sayur-sayuran","Sayur-sayuran"),
        ("Perkebunan","Perkebunan")
    ]
    daerah = models.ForeignKey(Pemerintah, on_delete=models.CASCADE)
    nama_tanaman = models.CharField(max_length=32, blank=False, null=False, default="default_tanaman")
    jenis_tanaman = models.CharField(max_length=255, choices=JENIS, default="Biji-bijian")