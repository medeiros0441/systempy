from .CustomModelSerializer import CustomModelSerializer
from api.models import VendaModel, ItemCompraModel, ProdutoModel, ClienteModel, UsuarioModel,LojaModel
from rest_framework import serializers

class VendaSerializer(CustomModelSerializer):
    produtos = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ProdutoModel.objects.all()
    )
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=ClienteModel.objects.all(), allow_null=True
    )
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=UsuarioModel.objects.all(), allow_null=True
    )
    loja = serializers.PrimaryKeyRelatedField(
        queryset=LojaModel.objects.all()
    )
    
    class Meta(CustomModelSerializer.Meta):
        model = VendaModel
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
        queryset=VendaModel.objects.all(), allow_null=True
    )
    produto = serializers.PrimaryKeyRelatedField(
        queryset=ProdutoModel.objects.all(), allow_null=True
    )
    
    class Meta(CustomModelSerializer.Meta):
        model = ItemCompraModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_item_compra',
            'venda',
            'produto',
            'quantidade',
            'valor_unidade',
        ]
