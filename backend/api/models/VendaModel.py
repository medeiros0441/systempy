from .CustomModel import CustomModel
from django.db import models
from api.models import UsuarioModel,ClienteModel,ProdutoModel,EmpresaModel,LojaModel
import uuid
from api.utils import Utils


class VendaModel(CustomModel):
    id_venda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_venda = models.CharField(
        default=Utils.obter_data_hora_atual, editable=False, max_length=100
    )
    DINHEIRO = 1
    MAQUINA_CREDITO = 2
    MAQUINA_DEBITO = 3
    PIX = 4
    FIADO = 5
    BOLETO = 6
    TIPO_PAGAMENTO_CHOICES = [
        (DINHEIRO, "Dinheiro"),
        (MAQUINA_CREDITO, "Máquina de Crédito"),
        (MAQUINA_DEBITO, "Máquina de Débito"),
        (PIX, "PIX"),
        (FIADO, "Fiado"),
        (BOLETO, "Boleto"),
    ]
    tipo_pagamento = models.IntegerField(
        choices=TIPO_PAGAMENTO_CHOICES, null=True, blank=True
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
    descricao = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(UsuarioModel, on_delete=models.SET_NULL, null=True)
    loja = models.ForeignKey(LojaModel, on_delete=models.CASCADE)
    cliente = models.ForeignKey(ClienteModel, on_delete=models.SET_NULL, null=True)
    produtos = models.ManyToManyField(ProdutoModel, through="ItemCompra", blank=True)
    nota_fiscal = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    def get_tipo_pagamento_display(self):
        return dict(self.TIPO_PAGAMENTO_CHOICES).get(
            self.tipo_pagamento, "Desconhecido"
        )
    class Meta:
        db_table="venda"


class ItemCompraModel(CustomModel):
    id_item_compra = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    venda = models.ForeignKey(VendaModel, on_delete=models.CASCADE, null=True)
    produto = models.ForeignKey(ProdutoModel, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField()
    valor_unidade = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    class Meta:
        db_table="item_compra"

class MotoboyModel(CustomModel):
    id_motoboy = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    empresa = models.ForeignKey(EmpresaModel, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table="motoboy"

class EntregaModel(CustomModel):
    id_entrega = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.OneToOneField(VendaModel, on_delete=models.CASCADE, related_name="entrega")
    valor_entrega = models.DecimalField(max_digits=10, decimal_places=2)
    time_pedido = models.TimeField(null=True, blank=True)
    time_finalizacao = models.TimeField(null=True, blank=True)
    motoboy = models.ForeignKey(MotoboyModel, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    class Meta:
        db_table="entraga"