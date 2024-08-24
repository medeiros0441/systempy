from rest_framework import serializers
from api.models import ClienteModel, EnderecoModel, EmpresaModel
from .CustomModelSerializer import  CustomModelSerializer

class ClienteSerializer(CustomModelSerializer):
    endereco = serializers.PrimaryKeyRelatedField(queryset=EnderecoModel.objects.all())
    empresa = serializers.PrimaryKeyRelatedField(queryset=EmpresaModel.objects.all())

    class Meta(CustomModelSerializer.Meta):
        model = ClienteModel
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
