from django.db import models
from .cliente import Cliente
from .venda import Venda
from django.utils import timezone


class Galao(models.Model):
    id_galao = models.AutoField(
        primary_key=True,
    )
    data_insercao = models.DateTimeField()
    data_atualizacao = models.DateTimeField(null=True)
    data_validade = models.CharField(max_length=50)
    data_fabricacao = models.CharField(max_length=50)
    descricao = models.TextField(null=True)
    id_galao = models.AutoField(
        primary_key=True,
    )
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)


class GestaoGalao(models.Model):
    id_gestao_galao = models.AutoField(
        primary_key=True,
    )
    galao_saiu = models.ForeignKey(
        Galao,
        on_delete=models.CASCADE,
        related_name="galao_saiu_set",
        null=True,
    )
    galao_entrando = models.ForeignKey(
        Galao,
        on_delete=models.CASCADE,
        related_name="galao_entrando_set",
        null=True,
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True)
    insert = models.DateTimeField()
    update = models.DateTimeField(null=True)
