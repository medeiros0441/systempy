import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone

from ..utils import utils

class Historico(models.Model):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    descricao = models.TextField(blank=True, null=True)
    insert = models.CharField(default=utils.obter_data_hora_atual(), editable=False,  max_length=100) 
    update = models.CharField(default=utils.obter_data_hora_atual(), max_length=100)
    usuario = models.UUIDField(
        Usuario,
    )
