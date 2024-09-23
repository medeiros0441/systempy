from rest_framework import serializers
from datetime import datetime

class CustomModelSerializer(serializers.ModelSerializer):
    """
    Serializer base que inclui campos e métodos do CustomModel.
    """
    update = serializers.SerializerMethodField()

    def get_update(self, obj):
        """Método para retornar a data de atualização formatada."""
        if isinstance(obj.update, datetime):
            return obj.update.strftime('%d/%m/%Y %H:%M:%S')
        return None

    class Meta:
        fields = ['_insert', '_update', 'update']
        read_only_fields = ('insert', 'update')

    def format_errors(self, errors):
        """
        Recebe os erros do serializer e formata em uma string amigável.
        """
        formatted = []
        for field, field_errors in errors.items():
            # Verifica se existem vários erros para o mesmo campo
            if isinstance(field_errors, list):
                for error in field_errors:
                    formatted.append(f"{field}: {error}")
            else:
                formatted.append(f"{field}: {field_errors}")
        
        # Junta os erros com quebras de linha
        return "\n".join(formatted)
