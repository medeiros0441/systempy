from .CustomModelSerializer import CustomModelSerializer
from models import Log

class LogSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Log
        fields = CustomModelSerializer.Meta.fields + [
            'id_log',
            'tipo',
            'origem',
            'descricao',
            'usuario',
            'ip_usuario',
        ]
