from rest_framework import serializers
from ..models import Cliente, Endereco, Empresa
from .CustomModelSerializer import  CustomModelSerializer

class ClienteSerializer(CustomModelSerializer):
    endereco = serializers.PrimaryKeyRelatedField(queryset=Endereco.objects.all())
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())

    class Meta(CustomModelSerializer.Meta):
        model = Cliente
        fields = CustomModelSerializer.Meta.fields + [
            'id_cliente',
            'nome',
            'telefone',
            'ultima_compra',
            'tipo_cliente',
            'descricao',
            'endereco',
            'empresa',
        ]
