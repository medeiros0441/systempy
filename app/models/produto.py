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
    id_produto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(
        max_length=255,
    )
    quantidade_atual_estoque = models.IntegerField(null=True)
    quantidade_minima_estoque = models.IntegerField(null=True)
    codigo = models.IntegerField(null=True)
    is_retornavel = models.BooleanField(null=True,blank=True)

    data_validade = models.DateField(null=True,blank=True)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(default=timezone.now, null=True)
    preco_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    preco_venda = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    fabricante = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True)
    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
    )

    def preco_compra_f(self):
        return formatar_moeda(self.preco_compra)

    def preco_venda_f(self):
        return formatar_moeda(self.preco_venda)

    def quantidade_atual_estoque_f(self):
        return formatar_quantidade(self.quantidade_atual_estoque)

    def quantidade_minima_estoque_f(self):
        return formatar_quantidade(self.quantidade_minima_estoque)
