from django.db import models
from . import Usuario, Endereco, Empresa
from django.utils import timezone
import uuid


class Loja(models.Model):
    id_loja = models.AutoField(primary_key=True)
    nome_loja = models.CharField(max_length=255)
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
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(default=timezone.now, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)


class Associado(models.Model):
    id_associado = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(default=timezone.now, null=True)
    status_acesso = models.BooleanField(null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)
