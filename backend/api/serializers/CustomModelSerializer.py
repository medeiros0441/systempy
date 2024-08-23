
from CustomModelSerializer import CustomModelSerializer;
from rest_framework import serializers
from models import Configuracao,Usuario

class ConfiguracaoSerializer(CustomModelSerializer):
    
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta(CustomModelSerializer.Meta):
        model = Configuracao
        fields = CustomModelSerializer.Meta.fields + [
            'id_configuracao',
            'usuario',
            'codigo',
            'titulo',
            'descricao',
            'descricao_interna',
            'status_acesso',
        ]
