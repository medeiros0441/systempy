from CustomModelSerializer import CustomModelSerializer
from models import PDV,RegistroDiarioPDV,TransacaoPDV,AssociadoPDV

class PDVSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = PDV
        fields = CustomModelSerializer.Meta.fields + [
            'id_pdv',
            'nome',
            'loja',
            'saldo_inicial',
            'status_operacao',
        ]

class RegistroDiarioPDVSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = RegistroDiarioPDV
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
 

class TransacaoPDVSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = TransacaoPDV
        fields = CustomModelSerializer.Meta.fields + [
            'id_transacao',
            'registro_diario',
            'venda',
            'valor',
            'descricao',
            'tipo_operacao',
            'tipo_pagamento',
        ]
 

class AssociadoPDVSerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = AssociadoPDV
        fields = CustomModelSerializer.Meta.fields + [
            'id_associado',
            'status_acesso',
            'usuario',
            'pdv',
        ]
