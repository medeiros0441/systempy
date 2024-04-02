from django.db import models
from .usuario import Usuario
from .cliente import Cliente
from .produto import Produto
from .empresa import Empresa
from .loja import Loja
import uuid
from django.utils import timezone


class Venda(models.Model):
    id_venda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_venda = models.DateField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50)
    estado_transacao = models.CharField(max_length=20, null=True)
    metodo_entrega = models.CharField(max_length=50, null=True, blank=True)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    loja = models.ForeignKey("Loja", on_delete=models.CASCADE)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    # Campos relacionados ao troco
    valor_pago = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    troco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nota_fiscal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Venda {self.id_venda}"


class Compra(models.Model):
    id_compra = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    produtos = models.ManyToManyField(Produto, through="ItemCompra")
    data_compra = models.DateField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50)
    estado_transacao = models.CharField(max_length=20, null=True)
    numero_transacao = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    metodo_entrega = models.CharField(max_length=50, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Se o objeto já existe no banco de dados, atualize o campo "update"
        if self.pk:
            self.update = timezone.now()
        super().save(*args, **kwargs)


class ItemCompra(models.Model):
    id_item_compra = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.produto} ({self.quantidade})"

    def save(self, *args, **kwargs):
        if self.pk:
            self.update = timezone.now()
        super().save(*args, **kwargs)


class Motoboy(models.Model):
    id_motoboy = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)


class Entrega(models.Model):
    id_entrega = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.OneToOneField(
        Venda, on_delete=models.CASCADE, related_name="entrega"
    )
    valor_entrega = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(default=timezone.now)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    motoboy = models.ForeignKey(
        Motoboy, on_delete=models.SET_NULL, null=True, blank=True
    )


class Caixa(models.Model):
    id_caixa = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    insert = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_final = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )


class Transacao(models.Model):
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
