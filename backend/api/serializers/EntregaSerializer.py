from .CustomModelSerializer import CustomModelSerializer
from api.models import EntregaModel, VendaModel, MotoboyModel
from rest_framework import serializers

class MotoboySerializer(CustomModelSerializer):
    class Meta(CustomModelSerializer.Meta):
        model = MotoboyModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_motoboy',
            'nome',
            'numero',
            'empresa',
        ] 

class EntregaSerializer(CustomModelSerializer):
    venda = serializers.PrimaryKeyRelatedField(
        queryset=VendaModel.objects.all()
    )
    motoboy = serializers.PrimaryKeyRelatedField(
        queryset=MotoboyModel.objects.all(), allow_null=True
    )
    
    class Meta(CustomModelSerializer.Meta):
        model = EntregaModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_entrega',
            'venda',
            'valor_entrega',
            'time_pedido',
            'time_finalizacao',
            'motoboy',
            'descricao',
        ]
