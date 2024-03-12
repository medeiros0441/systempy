from django.db import models
from .usuario import Usuario
from .cliente import Cliente
from .produto import Produto
import uuid


class Venda(models.Model):
    id_venda = (models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),)
    data_venda = models.DateField()
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    forma_pagamento = models.CharField(
        max_length=50,
    )
    tipo_venda = models.CharField(
        max_length=20,
    )
    insert = models.DateTimeField()
    update = models.DateTimeField(null=True)
    descricao = models.TextField()
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
    )
    loja = models.ForeignKey(
        "Loja",
        on_delete=models.CASCADE,
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
    )


class VendaProduto(models.Model):
    id_venda_produto = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        to_field="id_produto",
    )
    quantidade = models.IntegerField()
    insert = models.DateTimeField()
    update = models.DateTimeField(null=True)
