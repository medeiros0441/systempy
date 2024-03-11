import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone


class Configuracao(models.Model):
    id_configuracao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    usuario = models.UUIDField(Usuario, db_column="id")
    titulo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    descricao_intera = models.TextField(blank=True, null=True)
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(
        db_column="date_time_update", default=timezone.now, null=True
    )
    status = models.BooleanField(default=True)
