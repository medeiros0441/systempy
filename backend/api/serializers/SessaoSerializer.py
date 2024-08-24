from .CustomModelSerializer import CustomModelSerializer
from api.models import SessaoModel

class SessaoSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = SessaoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_sessao',
            'id',
            'ip_sessao',
            'descricao',
            'pagina_atual',
            'time_iniciou',
            'status',
            'cidade',
            'regiao',
            'pais',
            'codigo_postal',
            'organizacao',
            'usuario',
        ]
