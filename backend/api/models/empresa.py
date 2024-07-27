from .CustomModel import CustomModel

from django.db import models

from django.utils import timezone
import uuid

from api.utils import Utils


class Empresa(CustomModel):

    id_empresa = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nome_empresa = models.TextField()
    nro_cnpj = models.TextField()
    razao_social = models.TextField(blank=True, null=True)
    descricao = models.TextField(null=True)
    nome_responsavel = models.TextField()
    cargo = models.TextField()
    email = models.EmailField()
    nro_cpf = models.TextField()
    telefone = models.TextField()
