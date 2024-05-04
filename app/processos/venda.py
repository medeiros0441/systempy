from builtins import int
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..utils import utils
from ..static import Alerta, UserInfo
from app import models 
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
import traceback
from django.db.models import F, Sum

class processos:

    def _processar_carrinho(carrinho, venda):
        try:
            # Criar um dicionário para armazenar as alterações no estoque do produto
            alteracoes_estoque = {}

            # Limpar os itens de compra associados a esta venda
            # venda.itens_compra.all().delete()

            # Iterar sobre os itens do carrinho
            for id_produto, quantidade in carrinho.items():
            # Obter o produto
                produto = models.Produto.objects.get(id_produto=id_produto)
                
                # Verificar se o produto já foi adquirido nesta venda
                item_comprado = models.ItemCompra.objects.filter(
                    produto_id=id_produto, venda_id=venda.id_venda
                ).first()
                
                if item_comprado:
                    # Se a quantidade for igual, não há alteração no carrinho
                    if item_comprado.quantidade == quantidade:
                        continue
                    
                    # Se a quantidade no carrinho for maior, capturar a diferença para cadastrar os produtos devolvidos
                    if item_comprado.quantidade < quantidade:
                        diferenca = quantidade - item_comprado.quantidade
                        produto.quantidade_atual_estoque += diferenca
                    # Se a quantidade no carrinho for menor, capturar a diferença para remover os produtos
                    else:
                        diferenca = item_comprado.quantidade - quantidade
                        produto.quantidade_atual_estoque -= diferenca
                    
                    produto.save()
                
                # Se o produto não foi adquirido anteriormente nesta venda, apenas atualizamos a quantidade em estoque
                else:
                    produto.quantidade_atual_estoque -= quantidade
                    produto.save()
                # Criar o item de compra
                models.ItemCompra.objects.update_or_create(
                    venda=venda, produto=produto, defaults={"quantidade": quantidade})

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

    def criar_ou_atualizar_venda(dados):
        try:
            venda, created = models.Venda.objects.update_or_create(
                id_venda=dados['id_venda'],
                defaults={
                    'forma_pagamento': dados['forma_pagamento'],
                    'estado_transacao': dados['estado_transacao'],
                    'metodo_entrega': dados['metodo_entrega'],
                    'desconto': dados['desconto'],
                    'valor_total': dados['valor_total'],
                    'valor_entrega': dados['taxa_entrega'],
                    'valor_pago': dados['valor_pago'],
                    'troco': dados['troco'],
                    'descricao': dados['desc_venda'],
                    'cliente': dados['cliente'],
                    'usuario': dados['user'],
                    'loja': dados['loja'],
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
                entrega = models.Entrega.objects.get(id_entrega=id_entrega)
                entrega.time_finalizacao = timezone.now().time()
                entrega.save()
                return True  # Retorna True em caso de sucesso
            elif "venda" in kwargs and "id_motoboy" in kwargs:
                # Criar uma nova entrega ou atualizar se já existir
                venda = kwargs["venda"]
                id_motoboy = kwargs["id_motoboy"]
                valor_entrega = processos.converter_para_decimal(venda.valor_entrega)
                
                entrega, created = models.Entrega.objects.update_or_create(
                    venda=venda,
                    defaults={
                        'valor_entrega': valor_entrega,
                        'time_pedido': timezone.now().time(),
                        'motoboy_id': id_motoboy,
                    }
                )
                return True  # Retorna True em caso de sucesso
            else:
                raise ValueError("Parâmetros inválidos para processo_entrega")
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
            return models.Caixa.objects.get(loja_id=loja_id, insert__date=hoje)
        except ObjectDoesNotExist:
            caixa_atual = models.Caixa.objects.create(loja_id=loja_id, saldo_inicial=100)
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
        models.Transacao.objects.create(
            caixa=caixa_atual,
            venda=venda,
            valor=valor_entrada,
            descricao=descricao_entrada,
        )
        models.Transacao.objects.create(
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
                        galao_entrada, created_entrada = models.Galao.objects.get_or_create(
                            data_validade=entrada["data_validade"],
                            data_fabricacao=entrada["data_fabricacao"],
                            titulo=entrada["titulo"],
                            loja=venda.loja,
                        )

                        galao_saida, created_saida = models.Galao.objects.get_or_create(
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
                    gestao_galao = models.GestaoGalao()
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
