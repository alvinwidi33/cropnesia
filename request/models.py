from django.db import models
from user.models import Pemerintah
from hasil_pertanian.models import HasilPertanian
class Request(models.Model):
    STATUS =[
        ("Terima", "Terima"),
        ("Tolak", "Tolak"),
        ("Belum Dikonfirmasi","Belum Dikonfirmasi")
    ]
    id_pemerintah_request = models.ForeignKey(Pemerintah, on_delete=models.CASCADE)
    id_hasil_pertanian = models.OneToOneField(HasilPertanian, on_delete=models.CASCADE)
    status_request = models.CharField(max_length=32, choices=STATUS, default="Belum Dikonfirmasi")
    datetime_request=models.DateTimeField(auto_now=True)