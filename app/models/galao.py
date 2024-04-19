from django.db import models
from .cliente import Cliente
from .venda import Venda
from .loja import Loja
from django.utils import timezone


class Galao(models.Model):
    id_galao = models.AutoField(primary_key=True)
    data_validade = models.CharField(max_length=50, null=True)
    data_fabricacao = models.CharField(max_length=50, null=True)
    descricao = models.TextField(null=True)
    quantidade = models.IntegerField(default=0)  # Quantidade de galões
    titulo = models.CharField(max_length=100, null=True)  # Título do galão
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True)


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
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True)
    descricao = models.TextField(null=True)
