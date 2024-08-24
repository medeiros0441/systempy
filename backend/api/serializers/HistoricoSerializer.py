from .CustomModelSerializer import CustomModelSerializer
from api.models import HistoricoAlteracoesModel,HistoricoModel

class HistoricoSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = HistoricoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_historico',
            'descricao',
            'usuario',
        ]

class HistoricoAlteracoesSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = HistoricoAlteracoesModel
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
