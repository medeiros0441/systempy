
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..def_global import erro, criar_alerta_js,verificar_permissoes
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
    Entrega
)
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
class processos():
        
    def _processar_carrinho(list_carrinho, venda):
        try:
            for item_carrinho in list_carrinho.getlist("item_carrinho"):
                id_produto, quantidade = item_carrinho.split("|")
                
                # Obtenha o produto de forma síncrona
                produto = Produto.objects.get(id_produto=id_produto)
                
                # Criar os itens de compra associados à venda de forma síncrona
                ItemCompra.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade
                )
        except Exception as e:
            # Trate possíveis erros
            print(f"Erro ao processar carrinho: {e}")
            raise 
                    
    def _processar_venda(data_formulario, id):
        # Função para converter um valor para decimal e tratar exceções
        def converter_para_decimal(valor):
            try:
                return Decimal(valor.replace(',', '.'))
            except (ValueError, TypeError):
                return None

        try:
            # Validando os dados do formulário
            estado_transacao = data_formulario.get('estado_transacao')
            forma_pagamento = data_formulario.get('forma_pagamento')
            desconto = data_formulario.get('desconto', None)

            metodo_entrega = data_formulario.get('metodo_entrega', '').strip()
            taxa_entrega = data_formulario.get('taxa_entrega', '').strip()
            if metodo_entrega != "0":
                if metodo_entrega == "entrega_no_local":
                    taxa_entrega_decimal = converter_para_decimal(taxa_entrega)
                    if taxa_entrega_decimal is None or taxa_entrega_decimal <= 0:
                        return None, 'Taxa de entrega inválida.'

            if estado_transacao == "0" or forma_pagamento == "0":
                return None, 'Estado da transação ou forma de pagamento inválidos.'

            if forma_pagamento == "dinheiro":
                valor_pago = data_formulario.get('valor_pago').strip()
                total_apagar = data_formulario.get('total_apagar').strip()
                valor_pago = converter_para_decimal(valor_pago)
                total_apagar = converter_para_decimal(total_apagar)
                if valor_pago is None or total_apagar is None or valor_pago <= 0 or valor_pago < total_apagar:
                    return None, 'Valor pago inválido.'

            loja = data_formulario.get("loja")
            if loja == "0":
                return None, 'Loja não está selecionada.'

            id_cliente = data_formulario.get("id_cliente")
            if id_cliente == "0":
                id_cliente = None

            # Preenchendo campos relacionados ao troco, se aplicável
            valor_total =  data_formulario.get('total_apagar')
            valor_total = converter_para_decimal(valor_total)
            valor_pago = data_formulario.get('valor_pago')
            valor_pago = converter_para_decimal(valor_pago)
            troco = data_formulario.get('troco')
            troco = converter_para_decimal(troco)

            # Criando uma instância do modelo Venda com os dados do formulário de forma síncrona
            venda = Venda.objects.create(
                forma_pagamento=forma_pagamento,
                estado_transacao=estado_transacao,
                metodo_entrega=metodo_entrega,
                desconto=desconto,
                valor_total=total_apagar,
                valor_entrega=taxa_entrega,
                valor_pago=valor_pago,
                troco=troco,
                descricao=data_formulario.get('id_descricao'),
                cliente_id=id_cliente,
                usuario_id=id,
                loja_id=loja
            )

            return venda, None
        except Exception as e:
            # Trate possíveis erros
            print(f"Erro ao processar venda: {e}")
            return None, f"Erro ao processar venda: {e}"

    
    def processo_entrega(**kwargs):
        try:
            if 'id_entrega' in kwargs:
                # Atualizar o horário de finalização da entrega
                id_entrega = kwargs['id_entrega']
                entrega = Entrega.objects.get(id_entrega=id_entrega)
                entrega.time_finalizacao = timezone.now().time()
                entrega.save()
            elif 'venda' in kwargs and 'id_motoboy' in kwargs:
                # Criar uma nova entrega
                venda = kwargs['venda']
                id_motoboy = kwargs['id_motoboy']
                entrega = Entrega.objects.create(
                    venda=venda,
                    valor_entrega=venda.valor_entrega,
                    time_pedido=timezone.now().time(),
                    motoboy_id=id_motoboy
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
    @verificar_permissoes(codigo_model=11)
    def get_caixa_atual(loja_id):
        """
        Obtém o caixa atual para uma determinada loja.

        Parameters:
            loja_id (int): O ID da loja para a qual deseja-se obter o caixa.

        Returns:
            processos: O objeto de caixa atual.
        """
        hoje = date.today()
        try:
            return processos.objects.get(loja_id=loja_id, insert__date=hoje)
        except processos.DoesNotExist:
            caixa_atual = processos.objects.create(loja_id=loja_id, saldo_inicial=100)
            return caixa_atual

    @staticmethod
    @verificar_permissoes('Transacao')
    def atualizar_saldo(self, valor_entrada, valor_saida):
        """
        Atualiza o saldo do caixa com base nos valores de entrada e saída.

        Parameters:
            valor_entrada (Decimal): O valor de entrada no caixa.
            valor_saida (Decimal): O valor de saída do caixa.
        """
        self.saldo_final = self.saldo_inicial + valor_entrada - valor_saida
        self.save()

    @staticmethod
    @verificar_permissoes("Caixa")
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
    @verificar_permissoes('caixa')
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
        processos.objects.create(caixa=caixa_atual, venda=venda, valor=valor_entrada, descricao=descricao_entrada)
        processos.objects.create(caixa=caixa_atual, venda=venda, valor=valor_saida, descricao=descricao_saida)

        # Atualizar o saldo final do caixa
        caixa_atual.atualizar_saldo(valor_entrada, valor_saida)
    
    def _processar_dados_galoes(request, venda, cliente):
        if request.method == "POST":
            try:
                data_galao_entrada = data_fabricacao_entrada = tipo_entrada = data_galao_saida = data_fabricacao_saida = tipo_saida = descricao = None

                for chave, valor in request.POST.items():
                    if chave.startswith("data_validade_entrada_"):
                        data_galao_entrada = datetime.strptime(valor, "%m/%Y").date()
                    elif chave.startswith("data_fabricacao_entrada_"):
                        data_fabricacao_entrada = datetime.strptime(valor, "%m/%Y").date()
                    elif chave.startswith("tipo_entrada_"):
                        tipo_entrada = valor
                    elif chave.startswith("data_validade_saida_"):
                        data_galao_saida = datetime.strptime(valor, "%m/%Y").date()
                    elif chave.startswith("data_fabricacao_saida_"):
                        data_fabricacao_saida = datetime.strptime(valor, "%m/%Y").date()
                    elif chave.startswith("tipo_saida_"):
                        tipo_saida = valor
                    elif chave.startswith("id_descricao_gestão_galao"):
                        descricao = valor

                # Crie galões de entrada e saída
                galao_entrada, created_entrada = Galao.objects.get_or_create(
                    data_validade=parse_date(data_galao_entrada),
                    titulo=tipo_entrada,
                    loja=venda.loja,
                )
                galao_saida, created_saida = Galao.objects.get_or_create(
                    data_validade=parse_date(data_galao_saida),
                    titulo=tipo_saida,
                    loja=venda.loja,
                )

                # Atualizar as quantidades
                if created_entrada:
                    galao_entrada.quantidade = 1
                else:
                    galao_entrada.quantidade += 1

                galao_entrada.update = timezone.now()
                galao_entrada.save()

                if created_saida:
                    galao_saida.quantidade = -1
                else:
                    galao_saida.quantidade -= 1
                galao_saida.update = timezone.now()
                galao_saida.save()

                # Criar um objeto GestaoGalao
                gestao_galao = GestaoGalao()
                gestao_galao.descricao = descricao
                gestao_galao.galao_entrando = galao_entrada
                gestao_galao.galao_saiu = galao_saida
                gestao_galao.venda = venda
                gestao_galao.cliente = cliente
                gestao_galao.update = timezone.now()
                gestao_galao.save()

                return True
            except Exception as e:
                # Tratar possíveis erros
                print(f"Erro ao processar dados dos galões: {e}")
                return False