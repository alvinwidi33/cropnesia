from datetime import datetime
from django.db import models
from tanaman.models import Tanaman

class HasilPertanian(models.Model):
    STATUS = [
        ("Gagal Panen", "Gagal Panen"),
        ("Berhasil Panen", "Berhasil Panen"),
        ("Kosong","Kosong")
    ]
    id_tanaman = models.OneToOneField(Tanaman, on_delete=models.CASCADE)
    kuantitas = models.FloatField(null=False, blank=False, default=0)
    harga_hasil_pertanian = models.FloatField(null=False, blank=False, default=0)
    status_panen = models.CharField(max_length=32, choices=STATUS, default="Kosong")
    datetime_panen = models.DateTimeField(default=datetime.now, null=False, blank=False)
