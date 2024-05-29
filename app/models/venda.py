from django.db import models
from .usuario import Usuario
from .cliente import Cliente
from .produto import Produto
from .empresa import Empresa
from .loja import Loja
import uuid
from django.utils import timezone
from app.utils import Utils


class Venda(models.Model):
    id_venda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_venda = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    forma_pagamento = models.CharField(max_length=50)
    estado_transacao = models.CharField(max_length=20, null=True)
    metodo_entrega = models.CharField(max_length=50, null=True, blank=True)
    desconto = models.CharField(max_length=50, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_entrega = models.CharField(max_length=50, null=True, blank=True)
    valor_pago = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    troco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    descricao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    produtos = models.ManyToManyField(Produto, through="ItemCompra", blank=True)
    nota_fiscal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)


class ItemCompra(models.Model):
    id_item_compra = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField()
    valor_unidade = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)


class Motoboy(models.Model):
    id_motoboy = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)


class Entrega(models.Model):
    id_entrega = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.OneToOneField(
        Venda, on_delete=models.CASCADE, related_name="entrega"
    )
    valor_entrega = models.DecimalField(max_digits=10, decimal_places=2)
    time_pedido = models.TimeField(null=True, blank=True)
    time_finalizacao = models.TimeField(null=True, blank=True)
    insert = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    update = models.CharField(default=Utils.obter_data_hora_atual, max_length=100)
    motoboy = models.ForeignKey(
        Motoboy, on_delete=models.SET_NULL, null=True, blank=True
    )
    descricao = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.update = Utils.obter_data_hora_atual()
        super().save(*args, **kwargs)
