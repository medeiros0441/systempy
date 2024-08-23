from .CustomModelSerializer import CustomModelSerializer
from models import Entrega, Venda, Motoboy
from rest_framework import serializers

class MotoboySerializer(CustomModelSerializer):
    class Meta(CustomModelSerializer.Meta):
        model = Motoboy
        fields = CustomModelSerializer.Meta.fields + [
            'id_motoboy',
            'nome',
            'numero',
            'empresa',
        ] 

class EntregaSerializer(CustomModelSerializer):
    venda = serializers.PrimaryKeyRelatedField(
        queryset=Venda.objects.all()
    )
    motoboy = serializers.PrimaryKeyRelatedField(
        queryset=Motoboy.objects.all(), allow_null=True
    )
    
    class Meta(CustomModelSerializer.Meta):
        model = Entrega
        fields = CustomModelSerializer.Meta.fields + [
            'id_entrega',
            'venda',
            'valor_entrega',
            'time_pedido',
            'time_finalizacao',
            'motoboy',
            'descricao',
        ]
