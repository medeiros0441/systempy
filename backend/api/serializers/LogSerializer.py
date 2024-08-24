from .CustomModelSerializer import CustomModelSerializer
from api.models import LogModel

class LogSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = LogModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_log',
            'tipo',
            'origem',
            'descricao',
            'usuario',
            'ip_usuario',
        ]
