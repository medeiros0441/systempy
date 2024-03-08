from django.db import models
from .usuario import Usuario
from .cliente import Cliente
from .produto import Produto
import uuid


class Venda(models.Model):
    id_venda = (
        models.UUIDField(
            primary_key=True, default=uuid.uuid4, db_column="id_venda", editable=False
        ),
    )
    data_venda = models.DateField(db_column="data_venda")
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="valor_total"
    )
    forma_pagamento = models.CharField(max_length=50, db_column="forma_pagamento")
    tipo_venda = models.CharField(max_length=20, db_column="tipo_venda")
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    descricao = models.TextField(db_column="descricao")
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, db_column="fk_usuario"
    )
    loja = models.ForeignKey("Loja", on_delete=models.CASCADE, db_column="fk_loja")
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, db_column="fk_cliente"
    )

    class Meta:
        db_table = "wms_venda"


class VendaProduto(models.Model):
    id_venda_produto = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_column="id_venda_produto",
        editable=False,
    )

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, db_column="fk_venda")
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, to_field="id_produto", db_column="fk_produto"
    )
    quantidade = models.IntegerField()
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)

    class Meta:
        db_table = "wms_venda_produto"
