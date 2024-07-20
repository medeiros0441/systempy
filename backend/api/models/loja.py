from django.db import models
from . import Usuario, Endereco, Empresa
from django.utils import timezone
import uuid
from api.utils import Utils


class Loja(models.Model):
    id_loja = models.AutoField(primary_key=True)
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
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)


class Associado(models.Model):
    id_associado = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    status_acesso = models.BooleanField(null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)
