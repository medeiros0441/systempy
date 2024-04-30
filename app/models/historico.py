import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone


class Historico(models.Model):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    descricao = models.TextField(blank=True, null=True)
    insert = models.DateTimeField(default=timezone.now, editable=False) 
    update = models.DateTimeField(auto_now=True)
    usuario = models.UUIDField(
        Usuario,
    )
