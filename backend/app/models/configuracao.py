import uuid
from django.db import models
from ..models.usuario import Usuario
from django.utils import timezone
from app.utils import Utils


class Configuracao(models.Model):
    id_configuracao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    codigo = models.IntegerField(null=True)
    titulo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    descricao_interna = models.TextField(blank=True, null=True)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    status_acesso = models.BooleanField(default=True)
