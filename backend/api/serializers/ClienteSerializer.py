from rest_framework import serializers
from api.models import ClienteModel, EnderecoModel, EmpresaModel
from .CustomModelSerializer import  CustomModelSerializer

class ClienteSerializer(CustomModelSerializer):
    empresa = serializers.PrimaryKeyRelatedField(queryset=EmpresaModel.objects.all())
    endereco = serializers.PrimaryKeyRelatedField(
        queryset=EnderecoModel.objects.all(),
        required=False,  # Permite que o campo seja opcional
        allow_null=True   # Permite valores nulos
    )
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
