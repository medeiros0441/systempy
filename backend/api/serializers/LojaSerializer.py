from .CustomModelSerializer import CustomModelSerializer
from api.models import LojaModel,AssociadoModel

class LojaSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = LojaModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_loja',
            'nome',
            'numero_telefone',
            'horario_operacao_inicio',
            'horario_operacao_fim',
            'segunda',
            'terca',
            'quarta',
            'quinta',
            'sexta',
            'sabado',
            'domingo',
            'empresa',
            'endereco',
        ]

class AssociadoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = AssociadoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_associado',
            'status_acesso',
            'usuario',
            'loja',
        ]
