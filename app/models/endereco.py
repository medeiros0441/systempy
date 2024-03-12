from django.db import models
from django.utils import timezone
import uuid


class Endereco(models.Model):
    id_endereco = models.AutoField(
        primary_key=True,
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    rua = models.CharField(
        max_length=255,
    )
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=30)
    descricao = models.TextField(null=True, max_length=500)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)
