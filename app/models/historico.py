import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone

class Historico(models.Model):
    id_historico = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    descricao = models.TextField(blank=True, null=True)
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(
        db_column="date_time_update", default=timezone.now, null=True
    )
    usuario = models.UUIDField(Usuario, db_column="id")


 