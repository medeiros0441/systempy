from .CustomModelSerializer import CustomModelSerializer
from models import Venda, ItemCompra, Produto, Cliente, ItemCompra, Venda, Produto,Usuario,Loja
from rest_framework import serializers

class VendaSerializer(CustomModelSerializer):
    produtos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Produto.objects.all()
    )
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), allow_null=True
    )
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), allow_null=True
    )
    loja = serializers.PrimaryKeyRelatedField(
        queryset=Loja.objects.all()
    )
    
    class Meta(CustomModelSerializer.Meta):
        model = Venda
        fields = CustomModelSerializer.Meta.fields + [
            'id_venda',
            'data_venda',
            'tipo_pagamento',
            'forma_pagamento',
            'estado_transacao',
            'metodo_entrega',
            'desconto',
            'valor_total',
            'valor_entrega',
            'valor_pago',
            'troco',
            'descricao',
            'usuario',
            'loja',
            'cliente',
            'produtos',
            'nota_fiscal',
        ]

class ItemCompraSerializer(CustomModelSerializer):
    venda = serializers.PrimaryKeyRelatedField(
        queryset=Venda.objects.all(), allow_null=True
    )
    produto = serializers.PrimaryKeyRelatedField(
        queryset=Produto.objects.all(), allow_null=True
    )
    
    class Meta(CustomModelSerializer.Meta):
        model = ItemCompra
        fields = CustomModelSerializer.Meta.fields + [
            'id_item_compra',
            'venda',
            'produto',
            'quantidade',
            'valor_unidade',
        ]
