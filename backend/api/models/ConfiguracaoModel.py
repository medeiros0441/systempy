import uuid
from .CustomModel import CustomModel
from django.db import models
from .UsuarioModel import UsuarioModel
from django.utils import timezone
from api.utils import Utils

class ConfiguracaoModel(CustomModel):
    id_configuracao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    usuario = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE, null=True)
    codigo = models.IntegerField(null=True)
    titulo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    descricao_interna = models.TextField(blank=True, null=True)
    status_acesso = models.BooleanField(default=True)
    class Meta:
        db_table = 'configuracao'