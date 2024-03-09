from django.db import models
from .loja import Loja
from django.utils import timezone
import uuid


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}" if valor is not None else ""


def formatar_quantidade(quantidade):
    if quantidade is not None:
        quantidade_str = str(quantidade)
        quantidade_formatada = ""
        count = 0
        for i in range(len(quantidade_str) - 1, -1, -1):
            quantidade_formatada = quantidade_str[i] + quantidade_formatada
            count += 1
            if count % 3 == 0 and i != 0:
                quantidade_formatada = "." + quantidade_formatada
        return f"{quantidade_formatada} Unidades"
    else:
        return ""


class Produto(models.Model):
    id_produto = models.UUIDField(
        primary_key=True, default=uuid.uuid4, db_column="id_produto", editable=False
    )
    nome = models.CharField(max_length=255, db_column="nome_produto")
    quantidade_atual_estoque = models.IntegerField(
        db_column="quantidade_atual_estoque", null=True
    )
    quantidade_minima_estoque = models.IntegerField(
        db_column="quantidade_minima_estoque", null=True
    )
    tipo = models.IntegerField(db_column="tipo_produto", null=True)
    insert = models.DateTimeField(db_column="date_time_insert", default=timezone.now)
    update = models.DateTimeField(
        db_column="date_time_update", default=timezone.now, null=True
    )
    preco_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="preco_compra",
        blank=True,
        null=True,
    )
    preco_venda = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="preco_venda",
        blank=True,
        null=True,
    )
    fabricante = models.CharField(max_length=100, db_column="fabricante", null=True)
    descricao = models.TextField(db_column="descricao", null=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, db_column="fk_loja")

    class Meta:
        db_table = "wms_produto"

    def preco_compra_f(self):
        return formatar_moeda(self.preco_compra)

    def preco_venda_f(self):
        return formatar_moeda(self.preco_venda)

    def quantidade_atual_estoque_f(self):
        return formatar_quantidade(self.quantidade_atual_estoque)

    def quantidade_minima_estoque_f(self):
        return formatar_quantidade(self.quantidade_minima_estoque)
