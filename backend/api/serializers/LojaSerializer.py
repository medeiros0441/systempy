from CustomModelSerializer import CustomModelSerializer
from models import Loja,Associado

class LojaSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Loja
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
        model = Associado
        fields = CustomModelSerializer.Meta.fields + [
            'id_associado',
            'status_acesso',
            'usuario',
            'loja',
        ]
