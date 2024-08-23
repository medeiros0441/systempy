from django.db import models
from django.utils import timezone
import uuid
from api.utils import Utils
from models import EmpresaModel,CustomModel


class UsuarioModel(CustomModel):
    id_usuario = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    nome_completo = models.CharField(max_length=255)
    nome_usuario = models.CharField(max_length=50)
    senha = models.CharField(max_length=200)
    nivel_usuario = models.IntegerField()
    status_acesso = models.BooleanField(default=False)
    email = models.EmailField(max_length=255)
    ultimo_login = models.DateTimeField(null=True)
    empresa = models.ForeignKey(EmpresaModel, on_delete=models.CASCADE)
    class Meta:
        dt_table="usuario"

class PersonalizacaoModel(CustomModel):
    id_personalizacao = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False
    )
    usuario = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE)
    chave = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    descricao_interna = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)
    class Meta:
        db_table="personalizacao"