
from models import Endereco
from CustomModelSerializer import CustomModelSerializer

class EnderecoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Endereco
        fields = CustomModelSerializer.Meta.fields + [
            'id_endereco',
            'id',
            'rua',
            'numero',
            'bairro',
            'cidade',
            'estado',
            'codigo_postal',
            'descricao',
        ]