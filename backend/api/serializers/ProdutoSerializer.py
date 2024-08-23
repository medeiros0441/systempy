from CustomModelSerializer import CustomModelSerializer
from models import Produto

class ProdutoSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = Produto
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
