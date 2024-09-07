from django.db import models
from .CustomModel import CustomModel
import uuid 
from .LojaModel import LojaModel

class ProdutoModel(CustomModel):
    id_produto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    quantidade_atual_estoque = models.IntegerField(null=True)
    quantidade_minima_estoque = models.IntegerField(null=True)
    codigo = models.PositiveIntegerField(unique=True, editable=False)
    is_retornavel = models.BooleanField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=True)
    data_validade = models.CharField(null=True, blank=True, max_length=50)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fabricante = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True)
    
    # Aqui, referenciando o modelo LojaModel como string
    loja = models.ForeignKey(
        LojaModel,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'produto'
