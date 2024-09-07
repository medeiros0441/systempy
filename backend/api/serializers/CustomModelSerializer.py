from rest_framework import serializers
from datetime import datetime

class CustomModelSerializer(serializers.ModelSerializer):
    """
    Serializer base que inclui campos e métodos do CustomModel.
    """
    # Exemplo de campo de método personalizado para a data de atualização formatada
    update = serializers.SerializerMethodField()

    def get_update(self, obj):
        """
        Método para retornar a data de atualização formatada.
        """
        if isinstance(obj.update, datetime):
            return obj.update.strftime('%d/%m/%Y %H:%M:%S')
        return None

    class Meta:
        fields = ['_insert', '_update', 'update']
        read_only_fields = ('_insert', '_update')
