import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone


class Configuracao(models.Model):
    id_configuracao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,null=True
    )
    titulo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    descricao_interna = models.TextField(blank=True, null=True)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(default=timezone.now, null=True)
    status_acesso = models.BooleanField(default=True)
