import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone


class Configuracao(models.Model):
    id_configuracao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    usuario = models.UUIDField(
        Usuario,
    )
    titulo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    descricao_intera = models.TextField(blank=True, null=True)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(default=timezone.now, null=True)
    status = models.BooleanField(default=True)
