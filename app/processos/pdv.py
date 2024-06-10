import uuid
from decimal import Decimal
from ..models import RegistroDiarioPDV, TransacaoPDV, PDV, AssociadoPDV
from django.core.exceptions import ObjectDoesNotExist
from ..static import UserInfo


class processos_pdv:
    def processar_transacao(request, modelo):
        id_usuario = UserInfo.get_id_usuario(request)
        id_empresa = UserInfo.get_id_empresa(request)
        if id_usuario or id_empresa is None:
            return False, "Usuario  Não está logado."
        # primeiro buscamos qual seria o ponto que o usuariop está associado.
        # depois de ter o ponto  vamos processar a trasacao no ponto correto.
        #
        pdv_id = AssociadoPDV.objects.filter(
            usuario_id=id_usuario, loja__empresa_id=id_empresa
        )
        pdv = PDV.objects.filter(id_pdv=pdv_id)

        if modelo.id_venda is None:
            return False
        return True

    def fechar_operacao(self):
        from utils import Utils

        # Obter o registro diário atual
        registro_diario = RegistroDiarioPDV.objects.filter(
            pdv=self, horario_fechamento__isnull=True
        ).first()

        if not registro_diario:
            raise Exception("Nenhum registro diário encontrado para fechar.")

        # Calcular totais de transações
        transacoes = TransacaoPDV.objects.filter(registro_diario=registro_diario)
        total_dinheiro = Decimal(0)
        total_maquina = Decimal(0)

        for transacao in transacoes:
            if transacao.venda:
                if transacao.venda.tipo_pagamento == "dinheiro":
                    total_dinheiro += transacao.valor
                elif transacao.venda.tipo_pagamento == "maquina":
                    total_maquina += transacao.valor

        # Atualizar registro diário
        registro_diario.saldo_final_dinheiro = (
            registro_diario.saldo_inicial_dinheiro + total_dinheiro
        )
        registro_diario.saldo_final_maquina = total_maquina
        registro_diario.saldo_final_total = (
            registro_diario.saldo_final_dinheiro + total_maquina
        )
        registro_diario.horario_fechamento = Utils.obter_data_hora_atual(True)
        registro_diario.update = Utils.obter_data_hora_atual()
        registro_diario.save()

        # Atualizar status do PDV
        self.status_operacao = False
        self.update = Utils.obter_data_hora_atual()
        self.save()

    @staticmethod
    def get_caixa_atual(loja_id):
        from utils import Utils

        hoje = Utils.obter_data_hora_atual(True)
        try:
            return PDV.objects.get(loja_id=loja_id, dia=hoje)
        except ObjectDoesNotExist:
            caixa_atual = PDV.objects.create(
                loja_id=loja_id, dia=hoje, saldo_inicial=100
            )
            return caixa_atual

    @staticmethod
    def atualizar_saldo(caixa_atual, valor_entrada, valor_saida):
        """
        Atualiza o saldo do caixa com base nos valores de entrada e saída.

        Parameters:
            valor_entrada (Decimal): O valor de entrada no caixa.
            valor_saida (Decimal): O valor de saída do PDV.
        """
        caixa_atual.saldo_final = (
            caixa_atual.saldo_inicial + valor_entrada - valor_saida
        )

        caixa_atual.save()

    @staticmethod
    def processar_caixa(venda):
        """
        Processa uma venda, adicionando transações ao caixa e atualizando o saldo.

        Parameters:
            venda (Venda): O objeto de venda a ser processado.
        """
        loja_id = venda.loja_id
        caixa_atual = AssociadoPDV.get_caixa_atual(loja_id)

        valor_entrada = venda.valor_pago
        valor_saida = venda.troco
        descricao_entrada = "Recebimento de venda"
        descricao_saida = "Troco de venda"

        # Adicionar transações ao caixa
        TransacaoPDV.objects.create(
            caixa=caixa_atual,
            venda=venda,
            valor=valor_entrada,
            descricao=descricao_entrada,
        )
        TransacaoPDV.objects.create(
            caixa=caixa_atual, venda=venda, valor=valor_saida, descricao=descricao_saida
        )

        # Atualizar o saldo final do caixa
        processos_pdv.atualizar_saldo(caixa_atual, valor_entrada, valor_saida)
