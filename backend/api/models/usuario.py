from .CustomModel import CustomModel
from django.db import models
from django.utils import timezone
import uuid
from api.utils import Utils
from .empresa import Empresa


class Usuario(CustomModel):
    id_usuario = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nome_completo = models.CharField(max_length=255)
    nome_usuario = models.CharField(max_length=50)
    senha = models.CharField(max_length=200)
    nivel_usuario = models.IntegerField()
    status_acesso = models.BooleanField(default=False)
    email = models.EmailField(max_length=255)
    ultimo_login = models.DateTimeField(null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)


class Personalizacao(CustomModel):
    id_personalizacao = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    chave = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    descricao_interna = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)
