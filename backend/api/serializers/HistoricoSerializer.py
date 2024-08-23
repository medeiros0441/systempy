from CustomModelSerializer import CustomModelSerializer
from models import Historico
from models import HistoricoAlteracoes

class HistoricoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Historico
        fields = CustomModelSerializer.Meta.fields + [
            'id_historico',
            'descricao',
            'usuario',
        ]

class HistoricoAlteracoesSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = HistoricoAlteracoes
        fields = CustomModelSerializer.Meta.fields + [
            'id_historico',
            'entidade',
            'entidade_id',
            'tipo_alteracao',
            'campo_alterado',
            'valor_antigo',
            'valor_novo',
            'usuario',
            'data_alteracao',
        ]
