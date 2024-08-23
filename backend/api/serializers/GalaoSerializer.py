from CustomModelSerializer import CustomModelSerializer
from models import Galao
from models import GestaoGalao

class GalaoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Galao
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
        model = GestaoGalao
        fields = CustomModelSerializer.Meta.fields + [
            'id_gestao_galao',
            'galao_saiu',
            'galao_entrando',
            'venda',
            'descricao',
        ]
