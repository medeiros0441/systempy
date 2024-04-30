import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone


class Log(models.Model):
    id_log = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(
        max_length=50
    )  # Tipo de log (Erro, Aviso, Informação, etc.)
    origem = models.CharField(
        max_length=100
    )  # Origem do log (nome do módulo, função, etc.)
    descricao = models.TextField()  # Descrição do log
    insert = models.DateTimeField(default=timezone.now, editable=False) 
    update = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
    )
    ip_usuario = models.CharField(max_length=50, blank=True, null=True)  # IP do cliente
