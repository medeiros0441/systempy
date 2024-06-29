import uuid
from decimal import Decimal
from ..models import RegistroDiarioPDV, TransacaoPDV, PDV, AssociadoPDV, Usuario, Venda
from django.core.exceptions import ObjectDoesNotExist
from ..static import UserInfo
from django.db.models import Sum
from django.db import transaction
from datetime import datetime
from ..utils import Utils


class processos_pdv:

    def abrir_registro_diario(pdv,usuario):
        today = Utils.obter_data_hora_atual("date")
        # Verifica se já existe um registro diário aberto para o PDV e o dia corrente
        registro_diario_aberto = RegistroDiarioPDV.objects.filter(pdv=pdv, dia=today, horario_fechamento__isnull=True).first()
        if registro_diario_aberto:
            return True, "já existe um registro diário aberto"

        # Cria um novo registro diário
        registro_diario = RegistroDiarioPDV(
            pdv=pdv,
            descricao_interna= " Abertura efetuada peo usuario "+usuario.nome_completo ,
            saldo_inicial_dinheiro=pdv.saldo_inicial,
            dia=today
        )
        registro_diario.save()
        
        pdv.status_operacao = PDV.ABERTO
        pdv.save()
        
        return registro_diario

    def fechar_registro_diario(registro_diario,usuario):
        with transaction.atomic():
            # Obtem todas as transações do registro diário
            transacoes = TransacaoPDV.objects.filter(registro_diario=registro_diario)

            saldo_dinheiro = 0
            saldo_maquina = 0

            for transacao in transacoes:
                if transacao.tipo_pagamento == TransacaoPDV.DINHEIRO:
                    if transacao.tipo_operacao == TransacaoPDV.ENTRADA:
                        saldo_dinheiro += transacao.valor
                    elif transacao.tipo_operacao == TransacaoPDV.RETIRADO:
                        saldo_dinheiro -= transacao.valor
                else:
                    if transacao.tipo_operacao == TransacaoPDV.ENTRADA:
                        saldo_maquina += transacao.valor
                    elif transacao.tipo_operacao == TransacaoPDV.RETIRADO:
                        saldo_maquina -= transacao.valor

            registro_diario.saldo_final_dinheiro = saldo_dinheiro
            registro_diario.saldo_final_maquina = saldo_maquina
            registro_diario.saldo_final_total = saldo_dinheiro + saldo_maquina
            registro_diario.descricao_interna =+ "- Registro fechado pelo associado -" +usuario.nome_completo
            registro_diario.horario_fechamento = Utils.obter_data_hora_atual("time")
            registro_diario.save()

            pdv = registro_diario.pdv
            pdv.status_operacao = PDV.FECHADO
            pdv.save()

        return registro_diario 

    def processar_transacao_PDV(data):
        """
        Processa uma transação no PDV com os dados fornecidos.
        """
        required_fields = [
            "registro_diario_id",
            "usuario_id",
            "venda_id",
            "valor",
            "descricao",
        ]

        # Verifica se todos os campos obrigatórios estão presentes
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return False, f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
        tipo_operacao = data["tipo_operacao"]
        registro_diario_id = data["registro_diario_id"]
        usuario_id = data["usuario_id"]
        venda_id = data["venda_id"]
        valor = data["valor"]
        descricao = data["descricao"]

        # Verifica se os IDs fornecidos são válidos
        status, message = processos_pdv.verificar_ids(
            usuario_id, venda_id, registro_diario_id
        )
        if not status:
            return False, message

        # Tenta criar a transação no PDV
        try:
            TransacaoPDV.objects.create(
                registro_diario_id=registro_diario_id,
                usuario_id=usuario_id,
                venda_id=venda_id,
                valor=valor,
                descricao=descricao,
                tipo_operacao=tipo_operacao,
            )
            return True, "Transação processada com sucesso"
        except Exception as e:
            return False, f"Erro ao processar a transação: {str(e)}"

    def verificar_ids(usuario_id, venda_id, registro_diario_id):
        """
        Verifica se os IDs fornecidos existem no banco de dados.
        """
        try:
            RegistroDiarioPDV.objects.get(pk=registro_diario_id)
        except RegistroDiarioPDV.DoesNotExist:
            return False, "registro_diario_id não é válido"

        try:
            Usuario.objects.get(pk=usuario_id)
        except Usuario.DoesNotExist:
            return False, "usuario_id não é válido"

        try:
            Venda.objects.get(pk=venda_id)
        except Venda.DoesNotExist:
            return False, "venda_id não é válido"

        return True, "IDs verificados com sucesso"

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
