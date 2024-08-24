from .CustomModelSerializer import CustomModelSerializer
from api.models import ProdutoModel

class ProdutoSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = ProdutoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_produto',
            'nome',
            'quantidade_atual_estoque',
            'quantidade_minima_estoque',
            'codigo',
            'is_retornavel',
            'status',
            'data_validade',
            'preco_compra',
            'preco_venda',
            'fabricante',
            'descricao',
            'loja',
        ]
