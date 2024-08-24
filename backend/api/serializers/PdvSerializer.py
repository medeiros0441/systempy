from .CustomModelSerializer import CustomModelSerializer
from api.models import PdvModel,RegistroDiarioPdvModel,TransacaoPdvModel,AssociadoPdvModel

class PdvSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = PdvModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_pdv',
            'nome',
            'loja',
            'saldo_inicial',
            'status_operacao',
        ]

class RegistroDiarioPdvSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = RegistroDiarioPdvModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_registro_diario',
            'pdv',
            'dia',
            'saldo_inicial_dinheiro',
            'saldo_final_dinheiro',
            'saldo_final_total',
            'maquina_tipo',
            'saldo_final_maquina',
            'horario_iniciou',
            'horario_fechamento',
            'descricao_interna',
        ]
 

class TransacaoPdvSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = TransacaoPdvModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_transacao',
            'registro_diario',
            'venda',
            'valor',
            'descricao',
            'tipo_operacao',
            'tipo_pagamento',
        ]
 

class AssociadoPdvSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = AssociadoPdvModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_associado',
            'status_acesso',
            'usuario',
            'pdv',
        ]
