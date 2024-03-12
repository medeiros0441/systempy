from django.db import models
from .empresa import Empresa
from .endereco import Endereco
from django.utils import timezone


class Loja(models.Model):
    id_loja = models.AutoField(
        primary_key=True,
    )
    nome_loja = models.CharField(
        max_length=255,
    )
    numero_telefone = models.CharField(max_length=50, null=True)

    horario_operacao_inicio = models.TimeField(
        null=True,
        blank=True,
    )
    horario_operacao_fim = models.TimeField(
        null=True,
        blank=True,
    )
    segunda = models.BooleanField(
        default=False,
    )
    terca = models.BooleanField(
        default=False,
    )
    quarta = models.BooleanField(
        default=False,
    )
    quinta = models.BooleanField(
        default=False,
    )
    sexta = models.BooleanField(
        default=False,
    )
    sabado = models.BooleanField(
        default=False,
    )
    domingo = models.BooleanField(
        default=False,
    )

    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(default=timezone.now, null=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
    )
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
