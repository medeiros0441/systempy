import uuid
from api.utils import Utils
from .CustomModel import CustomModel

from django.db import models
from .UsuarioModel import  UsuarioModel
from .VendaModel import  VendaModel

class PdvModel(CustomModel):
    EXCLUIDO = 0
    ABERTO = 1
    FECHADO = 2
    BLOQUEADO = 3

    STATUS_OPERACAO_CHOICES = [
        (BLOQUEADO, "Bloqueado"),
        (EXCLUIDO, "Excluído"),
        (ABERTO, "Aberto"),
        (FECHADO, "Fechado"),
    ]

    id_pdv = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, null=True)
    loja = models.ForeignKey("Loja", on_delete=models.CASCADE)

    saldo_inicial = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    status_operacao = models.IntegerField(
        choices=STATUS_OPERACAO_CHOICES, default=FECHADO
    )
    class Meta:
        db_table = 'pdv'

class RegistroDiarioPdvModel(CustomModel):
    id_registro_diario = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    pdv = models.ForeignKey(PdvModel, on_delete=models.CASCADE, editable=False)
    dia = models.CharField(
        editable=False, null=True, max_length=50, default=Utils.obter_data_hora_atual
    )
    saldo_inicial_dinheiro = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0, null=True
    )
    saldo_final_dinheiro = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    saldo_final_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    maquina_tipo = models.CharField(max_length=50, null=True, blank=True)
    saldo_final_maquina = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    horario_iniciou = models.CharField(
        editable=False, default=Utils.obter_data_hora_atual, max_length=50
    )
    horario_fechamento = models.CharField(max_length=50, null=True, blank=True)
    descricao_interna = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        unique_together = (
            "pdv",
            "dia",
        )  # Garantir que não haja duplicatas de pdv e dia
        db_table = 'registro_diario_pdv'

class TransacaoPdvModel(CustomModel):
    id_transacao = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    registro_diario = models.ForeignKey(
        RegistroDiarioPdvModel, on_delete=models.CASCADE, blank=True
    )
    venda = models.ForeignKey(VendaModel, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=100)

    ENTRADA = 1
    RETIRADO = 2

    TIPO_OPERACAO_CHOICES = [
        (ENTRADA, "Entrou"),
        (RETIRADO, "Retirado"),
    ]
    tipo_operacao = models.IntegerField(
        choices=TIPO_OPERACAO_CHOICES, null=True, blank=True
    )
    DINHEIRO = 1
    MAQUINA_CREDITO = 2
    MAQUINA_DEBITO = 3
    PIX = 4
    FIADO = 5
    BOLETO = 6

    TIPO_PAGAMENTO_CHOICES = [
        (DINHEIRO, "Dinheiro"),
        (MAQUINA_CREDITO, "Máquina de Crédito"),
        (MAQUINA_DEBITO, "Máquina de Débito"),
        (PIX, "PIX"),
        (FIADO, "Fiado"),
        (BOLETO, "Boleto"),
    ]
    tipo_pagamento = models.IntegerField(
        choices=TIPO_PAGAMENTO_CHOICES, null=True, blank=True
    )
    class Meta:
        db_table = 'transacao_pdv'
class AssociadoPdvModel(CustomModel):
    id_associado = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    status_acesso = models.BooleanField(null=True)
    usuario = models.ForeignKey(UsuarioModel, on_delete=models.SET_NULL, null=True)
    pdv = models.ForeignKey(PdvModel, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'associado_pdv'
    

