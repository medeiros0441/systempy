from rest_framework import serializers

class CustomModelSerializer(serializers.ModelSerializer):
    """
    Serializer base que inclui campos e métodos do CustomModel.
    """
    # Adiciona o campo de data de atualização formatado
    update = serializers.SerializerMethodField()

    class Meta:
        fields = ['_insert', '_update', 'update']
        read_only_fields = ('_insert', '_update')
