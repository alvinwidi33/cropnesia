from django.db import models
from request.models import Request

class NegosiasiRequest(models.Model):
    id_request = models.OneToOneField(Request, on_delete=models.CASCADE)
    message = models.CharField(max_length=2048, blank=True, null=True, default="default_negosiasi")
    datetime_chat = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    def __str__(self):
        return f"NegosiasiRequest(id_request={self.id_request}, message={self.message}, datetime_chat={self.datetime_chat}, parent_id={self.parent_id})"

