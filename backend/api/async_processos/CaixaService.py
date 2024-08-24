# services.py

import asyncio
from django.core.exceptions import ObjectDoesNotExist
from api.models import PdvModel, AssociadoPdvModel, TransacaoPdvModel
from api.utils import Utils  # Supondo que Utils é um módulo utilitário que você tem

class CaixaService:

    @staticmethod
    async def get_caixa_atual(loja_id):
        """
        Obtém o caixa atual para uma loja específica. Se não existir, cria um novo caixa com saldo inicial.

        Parameters:
            loja_id (int): O ID da loja para a qual obter ou criar o caixa.

        Returns:
            PdvModel: O caixa atual para a loja.
        """
        hoje = Utils.obter_data_hora_atual(True)
        try:
            caixa_atual = await asyncio.to_thread(
                PdvModel.objects.get,
                loja_id=loja_id, dia=hoje
            )
            return caixa_atual
        except ObjectDoesNotExist:
            caixa_atual = await asyncio.to_thread(
                PdvModel.objects.create,
                loja_id=loja_id, dia=hoje, saldo_inicial=100
            )
            return caixa_atual

    @staticmethod
    async def atualizar_saldo(caixa_atual, valor_entrada, valor_saida):
        """
        Atualiza o saldo do caixa com base nos valores de entrada e saída.

        Parameters:
            caixa_atual (PdvModel): O caixa a ser atualizado.
            valor_entrada (Decimal): O valor de entrada no caixa.
            valor_saida (Decimal): O valor de saída do caixa.
        """
        caixa_atual.saldo_final = (
            caixa_atual.saldo_inicial + valor_entrada - valor_saida
        )
        await asyncio.to_thread(caixa_atual.save)

    @staticmethod
    async def processar_caixa(venda):
        """
        Processa uma venda, adicionando transações ao caixa e atualizando o saldo.

        Parameters:
            venda (Venda): O objeto de venda a ser processado.
        """
        loja_id = venda.loja_id
        caixa_atual = await CaixaService.get_caixa_atual(loja_id)

        valor_entrada = venda.valor_pago
        valor_saida = venda.troco
        descricao_entrada = "Recebimento de venda"
        descricao_saida = "Troco de venda"

        # Adicionar transações ao caixa
        await asyncio.to_thread(
            TransacaoPdvModel.objects.create,
            caixa=caixa_atual,
            venda=venda,
            valor=valor_entrada,
            descricao=descricao_entrada
        )
        await asyncio.to_thread(
            TransacaoPdvModel.objects.create,
            caixa=caixa_atual,
            venda=venda,
            valor=valor_saida,
            descricao=descricao_saida
        )

        # Atualizar o saldo final do caixa
        await CaixaService.atualizar_saldo(caixa_atual, valor_entrada, valor_saida)
