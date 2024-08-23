from CustomModelSerializer import CustomModelSerializer
from models import Sessao

class SessaoSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = Sessao
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
