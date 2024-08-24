from django.db import models
from .CustomModel import CustomModel
import uuid
from .EmpresaModel import EmpresaModel
from .EnderecoModel import EnderecoModel 
from .UsuarioModel import UsuarioModel


class LojaModel(CustomModel):
    id_loja = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    numero_telefone = models.CharField(max_length=50, null=True)
    horario_operacao_inicio = models.TimeField(null=True, blank=True)
    horario_operacao_fim = models.TimeField(null=True, blank=True)
    segunda = models.BooleanField(default=False)
    terca = models.BooleanField(default=False)
    quarta = models.BooleanField(default=False)
    quinta = models.BooleanField(default=False)
    sexta = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)
    empresa = models.ForeignKey('EmpresaModel', on_delete=models.CASCADE)
    endereco = models.ForeignKey('EnderecoModel', on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'loja'

class AssociadoModel(CustomModel):
    id_associado = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status_acesso = models.BooleanField(null=True)
    usuario = models.ForeignKey('UsuarioModel', on_delete=models.CASCADE, null=True)
    loja = models.ForeignKey('LojaModel', on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'loja_associado'