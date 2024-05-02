from builtins import int
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..utils import utils
from ..static import Alerta, UserInfo
from ..models import (
    Venda,
    Configuracao,
    Usuario,
    Associado,
    Loja,
    Cliente,
    Produto,
    ItemCompra,
    Transacao,
    Caixa,
    GestaoGalao,
    Galao,
    Entrega,
)
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
import traceback


class processos:

    def _processar_carrinho(list_carrinho, venda):
        try:
            for item_carrinho in list_carrinho.getlist("item_carrinho"):
                id_produto, quantidade = item_carrinho.split("|")
                quantidade = int(quantidade)
                # Obtenha o produto de forma síncrona
                produto = Produto.objects.get(id_produto=id_produto)

                # Criar os itens de compra associados à venda de forma síncrona
                ItemCompra.objects.create(
                    venda=venda, produto=produto, quantidade=quantidade
                )

                valor_atual = produto.quantidade_atual_estoque - quantidade
                produto.quantidade_atual_estoque = valor_atual
                produto.save()
        except Exception as e:
            # Trate possíveis erros
            print(f"Erro ao processar carrinho: {e}")
            raise

    def converter_para_decimal(valor):
        try:
            if valor is None or valor == "":
                return Decimal(0)
            elif valor == "NaN":
                return Decimal(0)
            elif "," in valor:
                # Se houver vírgula no valor, substituímos por ponto e convertemos para Decimal
                valor = valor.replace(",", ".")
                return Decimal(valor)
            else:
                return Decimal(valor)
        except (ValueError, TypeError):
            return Decimal(0)

    def _processar_venda(data_formulario, id):
        # Função para converter um valor para decimal e tratar exceções

        try:
            # Validando os dados do formulário
            estado_transacao = data_formulario.get("estado_transacao")
            forma_pagamento = data_formulario.get("forma_pagamento")
            desconto = data_formulario.get("desconto", None)
            desconto = processos.converter_para_decimal(desconto)
            metodo_entrega = data_formulario.get("metodo_entrega", "").strip()
            taxa_entrega = data_formulario.get("taxa_entrega", "").strip()
            if metodo_entrega != "0":
                if metodo_entrega == "entrega_no_local":
                    taxa_entrega_decimal = processos.converter_para_decimal(
                        taxa_entrega
                    )
                    if taxa_entrega_decimal is None or taxa_entrega_decimal <= 0:
                        return None, "Taxa de entrega inválida."

            if estado_transacao == "0" or forma_pagamento == "0":
                return None, "Estado da transação ou forma de pagamento inválidos."

            valor_pago = data_formulario.get("valor_pago").strip()
            total_apagar = data_formulario.get("total_apagar").strip()
            valor_pago = processos.converter_para_decimal(valor_pago)
            total_apagar = processos.converter_para_decimal(total_apagar)
            troco = data_formulario.get("troco", 0.0)
            troco = processos.converter_para_decimal(troco)
            if forma_pagamento == "dinheiro":

                if (
                    valor_pago is None
                    or total_apagar is None
                    or valor_pago <= 0.0
                    or valor_pago < total_apagar
                ):
                    return None, "Valor pago inválido."
            else:
                valor_pago = total_apagar
            id_loja = data_formulario.get("loja")
            if id_loja == "0":
                return None, "Loja não está selecionada."
            loja = Loja.objects.get(id_loja=id_loja)
            id_cliente = data_formulario.get("id_cliente")
            if id_cliente != "0":
                cliente = Cliente.objects.get(id_cliente=id_cliente)
            else:
                cliente = None
            # Preenchendo campos relacionados ao troco, se aplicável
            valor_total = data_formulario.get("total_apagar")
            valor_total = processos.converter_para_decimal(valor_total)
            user = Usuario.objects.get(id_usuario=id)
            desc_venda = data_formulario.get("descricao_venda")
            print(data_formulario)

            id_venda = data_formulario.get("id_venda_editar",None)
            if id_venda == "":
                id_venda= None
            # Cria ou atualiza a venda conforme necessário
            venda, created = Venda.objects.update_or_create(
                id_venda=id_venda,
                defaults={
                    'forma_pagamento': forma_pagamento,
                    'estado_transacao': estado_transacao,
                    'metodo_entrega': metodo_entrega,
                    'desconto': desconto,
                    'valor_total': valor_total,
                    'valor_entrega': taxa_entrega,
                    'valor_pago': valor_pago,
                    'troco': troco,
                    'descricao': desc_venda,
                    'cliente': cliente,
                    'usuario': user,
                    'loja': loja,
                }
            )

            return venda, None
        except Exception as e:
            # Trate possíveis erros
            print(f"Erro ao processar venda: {e}")
            traceback.print_exc()  # Adiciona esta linha para imprimir o traceback
            return None, f"Erro ao processar venda: {e}"

    def processo_entrega(**kwargs):
        try:
            if "id_entrega" in kwargs:
                # Atualizar o horário de finalização da entrega
                id_entrega = kwargs["id_entrega"]
                entrega = Entrega.objects.get(id_entrega=id_entrega)
                entrega.time_finalizacao = timezone.now().time()
                entrega.save()
            elif "venda" in kwargs and "id_motoboy" in kwargs:
                # Criar uma nova entrega
                venda = kwargs["venda"]
                id_motoboy = kwargs["id_motoboy"]
                entrega = Entrega.objects.create(
                    venda=venda,
                    valor_entrega=processos.converter_para_decimal(venda.valor_entrega),
                    time_pedido=timezone.now().time(),
                    motoboy_id=id_motoboy,
                )
            else:
                raise ValueError("Parâmetros inválidos para processo_entrega")

            return True  # Retorna True em caso de sucesso
        except ObjectDoesNotExist:
            # Tratar caso o objeto não seja encontrado
            return False
        except Exception as e:
            # Tratar outros erros inesperados
            print(f"Erro ao processar entrega: {e}")
            return False

    @staticmethod
    def get_caixa_atual(loja_id):

        hoje = date.today()
        try:
            return Caixa.objects.get(loja_id=loja_id, insert__date=hoje)
        except ObjectDoesNotExist:
            caixa_atual = Caixa.objects.create(loja_id=loja_id, saldo_inicial=100)
            return caixa_atual

    @staticmethod
    def atualizar_saldo(caixa_atual, valor_entrada, valor_saida):
        """
        Atualiza o saldo do caixa com base nos valores de entrada e saída.

        Parameters:
            valor_entrada (Decimal): O valor de entrada no caixa.
            valor_saida (Decimal): O valor de saída do caixa.
        """
        caixa_atual.saldo_final = (
            caixa_atual.saldo_inicial + valor_entrada - valor_saida
        )

        caixa_atual.save()

    @staticmethod
    def fechar_caixa(self):
        """
        Fecha o caixa, calculando o saldo final com base nas transações e atualizando o registro.
        """
        # Encontrar todas as transações do caixa atual
        transacoes_caixa = processos.objects.filter(caixa=self)

        # Calcular o saldo final do caixa
        saldo_final = self.saldo_inicial
        for transacao in transacoes_caixa:
            saldo_final += transacao.valor

        # Atualizar o saldo final do caixa
        self.saldo_final = saldo_final
        self.save()

    @staticmethod
    def processar_caixa(venda):
        """
        Processa uma venda, adicionando transações ao caixa e atualizando o saldo.

        Parameters:
            venda (Venda): O objeto de venda a ser processado.
        """
        loja_id = venda.loja_id
        caixa_atual = processos.get_caixa_atual(loja_id)

        valor_entrada = venda.valor_pago
        valor_saida = venda.troco
        descricao_entrada = "Recebimento de venda"
        descricao_saida = "Troco de venda"

        # Adicionar transações ao caixa
        Transacao.objects.create(
            caixa=caixa_atual,
            venda=venda,
            valor=valor_entrada,
            descricao=descricao_entrada,
        )
        Transacao.objects.create(
            caixa=caixa_atual, venda=venda, valor=valor_saida, descricao=descricao_saida
        )

        # Atualizar o saldo final do caixa
        processos.atualizar_saldo(caixa_atual, valor_entrada, valor_saida)

    def _processar_dados_galoes(request, venda):
        if request.method == "POST":
            try:
                trocas = []
                # Iterar sobre as entradas do request.POST
                for chave, valor in request.POST.items():
                    if chave.startswith("data_validade_entrada_"):
                        # Extrair informações da entrada
                        indice = chave.split("_")[-1]
                        entrada = {
                            "data_validade": valor,
                            "data_fabricacao": request.POST[
                                f"data_fabricacao_entrada_{indice}"
                            ],
                            "titulo": request.POST[f"tipo_entrada_{indice}"],
                        }

                        # Verificar se já existe uma troca para este índice
                        if len(trocas) <= int(indice):
                            trocas.append(
                                {"entradas": [], "saidas": [], "descricao": None}
                            )

                        # Adicionar a entrada à troca correspondente
                        trocas[int(indice)]["entradas"].append(entrada)

                    elif chave.startswith("data_validade_saida_"):
                        # Extrair informações da saída
                        indice = chave.split("_")[-1]
                        saida = {
                            "data_validade": valor,
                            "data_fabricacao": request.POST[
                                f"data_fabricacao_saida_{indice}"
                            ],
                            "titulo": request.POST[f"tipo_saida_{indice}"],
                        }

                        # Verificar se já existe uma troca para este índice
                        if len(trocas) <= int(indice):
                            trocas.append(
                                {"entradas": [], "saidas": [], "descricao": None}
                            )

                        # Adicionar a saída à troca correspondente
                        trocas[int(indice)]["saidas"].append(saida)

                    elif chave == "id_descricao_gestão_galao":
                        # Adicionar a descrição à última troca
                        trocas[-1]["descricao"] = valor

                # Processar as trocas
                for troca in trocas:
                    # Processar cada entrada e saída da troca
                    for entrada, saida in zip(troca["entradas"], troca["saidas"]):
                        # Criar galões de entrada e saída
                        galao_entrada, created_entrada = Galao.objects.get_or_create(
                            data_validade=entrada["data_validade"],
                            data_fabricacao=entrada["data_fabricacao"],
                            titulo=entrada["titulo"],
                            loja=venda.loja,
                        )

                        galao_saida, created_saida = Galao.objects.get_or_create(
                            data_validade=saida["data_validade"],
                            data_fabricacao=saida["data_fabricacao"],
                            titulo=saida["titulo"],
                            loja=venda.loja,
                        )

                        # Atualizar as quantidades
                        galao_entrada.quantidade = (
                            1 if created_entrada else galao_entrada.quantidade + 1
                        )
                        galao_entrada.update = timezone.now()
                        galao_entrada.save()

                        galao_saida.quantidade = (
                            -1 if created_saida else galao_saida.quantidade - 1
                        )
                        galao_saida.update = timezone.now()
                        galao_saida.save()

                    # Criar um objeto GestaoGalao
                    gestao_galao = GestaoGalao()
                    gestao_galao.descricao = troca["descricao"]
                    gestao_galao.galao_entrando = galao_entrada
                    gestao_galao.galao_saiu = galao_saida
                    gestao_galao.venda = venda
                    gestao_galao.update = timezone.now()
                    gestao_galao.save()

                return True
            except Exception as e:
                # Tratar possíveis erros
                print(f"Erro ao processar dados dos galões: {e}")
                return False
