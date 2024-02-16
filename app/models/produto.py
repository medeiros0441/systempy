from django.db import models
from .loja import Loja


class Produto(models.Model):
    nome = models.CharField(max_length=255, db_column="nome_produto")
    quantidade_estoque = models.IntegerField(db_column="quantidade_estoque")
    tipo = models.IntegerField(db_column="tipo_produto")
    insert = models.DateTimeField(db_column="date_time_insert")
    update = models.DateTimeField(db_column="date_time_update", null=True)
    preco_compra = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="preco_compra"
    )
    preco_venda = models.DecimalField(
        max_digits=10, decimal_places=2, db_column="preco_venda"
    )
    fabricante = models.CharField(max_length=100, db_column="fabricante")
    descricao = models.TextField(db_column="descricao")
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, db_column="fk_loja")

    class Meta:
        db_table = "wms_produto"
