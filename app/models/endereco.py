from django.db import models
from django.utils import timezone
import uuid

from ..utils import utils

class Endereco(models.Model):
    id_endereco = models.AutoField(
        primary_key=True,
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    rua = models.CharField(
        max_length=255,
    )
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True)
    cidade = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=50, null=True)
    codigo_postal = models.CharField(max_length=30, null=True)
    descricao = models.TextField(null=True, max_length=500)
    insert = models.CharField(default=utils.obter_data_hora_atual(), editable=False,  max_length=100) 
    update = models.CharField(default=utils.obter_data_hora_atual(), max_length=100)
