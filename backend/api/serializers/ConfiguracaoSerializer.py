
from .CustomModelSerializer import CustomModelSerializer;
from rest_framework import serializers
from api.models import ConfiguracaoModel,UsuarioModel

class ConfiguracaoSerializer(CustomModelSerializer):
    
    usuario = serializers.PrimaryKeyRelatedField(queryset=UsuarioModel.objects.all())

    class Meta(CustomModelSerializer.Meta):
        model = ConfiguracaoModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_configuracao',
            'usuario',
            'codigo',
            'titulo',
            'descricao',
            'descricao_interna',
            'status_acesso',
        ]
