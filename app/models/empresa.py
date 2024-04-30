from django.db import models
from django.utils import timezone
import uuid


class Empresa(models.Model):

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    id_empresa = models.AutoField(primary_key=True, )
    nome_empresa = models.TextField()
    nro_cnpj = models.TextField()
    razao_social = models.TextField(blank=True, null=True)
    descricao = models.TextField(null=True)
    nome_responsavel = models.TextField()
    cargo = models.TextField()
    email = models.EmailField()
    nro_cpf = models.TextField()
    telefone = models.TextField()
    insert = models.DateTimeField(default=timezone.now, editable=False) 
    update = models.DateTimeField(auto_now=True)

