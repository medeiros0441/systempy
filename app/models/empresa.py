from django.db import models
from django.utils import timezone
import uuid

from app.utils import Utils


class Empresa(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    id_empresa = models.AutoField(
        primary_key=True,
    )
    nome_empresa = models.TextField()
    nro_cnpj = models.TextField()
    razao_social = models.TextField(blank=True, null=True)
    descricao = models.TextField(null=True)
    nome_responsavel = models.TextField()
    cargo = models.TextField()
    email = models.EmailField()
    nro_cpf = models.TextField()
    telefone = models.TextField()
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
