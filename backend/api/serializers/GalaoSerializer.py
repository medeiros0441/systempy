from .CustomModelSerializer import CustomModelSerializer
from api.models import GestaoGalaoModel,GalaoModel

class GalaoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = GalaoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_galao',
            'data_validade',
            'data_fabricacao',
            'descricao',
            'quantidade',
            'titulo',
            'loja',
        ]

class GestaoGalaoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = GestaoGalaoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_gestao_galao',
            'galao_saiu',
            'galao_entrando',
            'venda',
            'descricao',
        ]
