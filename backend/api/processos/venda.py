from builtins import int
from datetime import date
from django.http import HttpResponse
from api.utils import Utils
from ..user import UserInfo
from api import models
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ObjectDoesNotExist
import traceback
from django.db.models import F, Sum
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class processos(APIView):
    permission_classes = [AllowAny]

    def converter_para_decimal(valor):
        try:
            return Decimal(valor)
        except (InvalidOperation, ValueError, TypeError):
            return None

    def _processar_carrinho(data, venda):
        try:
            # Criar um dicionário para armazenar as alterações no estoque do produto
            alteracoes_estoque = {}

            # Obter o carrinho de compras do objeto data
            carrinho = data.get("carrinho", [])

            # Garantir que carrinho seja uma lista
            if not isinstance(carrinho, list):
                carrinho = []

            # Função para verificar se um produto está no carrinho
            def produto_no_carrinho(id_produto_comprado, carrinho):
                for item in carrinho:
                    try:
                        id_produto = uuid.UUID(item.get("id_produto"))
                        if id_produto == id_produto_comprado:
                            return True
                    except (ValueError, TypeError):
                        continue
                return False

            # Obter todos os itens comprados relacionados a esta venda
            itens_comprados = models.ItemCompra.objects.filter(venda=venda)

            # Iterar sobre os itens comprados
            for item_comprado in itens_comprados:
                id_produto_comprado = item_comprado.produto.id_produto

                # Verificar se o produto comprado ainda está presente no carrinho
                if not produto_no_carrinho(id_produto_comprado, carrinho):
                    # Remover o item comprado se o produto não estiver mais no carrinho
                    produto = (
                        item_comprado.produto
                    )  # Evitar consulta adicional ao banco de dados
                    produto.quantidade_atual_estoque += item_comprado.quantidade
                    produto.save()
                    item_comprado.delete()

            for item in carrinho:
                id_produto = item.get("id_produto")
                quantidade = item.get("quantidade")

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
                    venda=venda,
                    produto=produto,
                    defaults={
                        "quantidade": quantidade,
                        "valor_unidade": produto.preco_venda,
                    },
                )

        except Exception as e:
            # Trate possíveis erros
            print(f"Erro ao processar carrinho: {e}")
            raise

    def criar_ou_atualizar_venda(dados):
        try:
            id_venda = dados.get("id_venda")

            if (
                id_venda and id_venda != ""
            ):  # Se o ID de venda for válido, fazemos um update
                try:
                    venda = models.Venda.objects.get(id_venda=id_venda)
                    venda.forma_pagamento = dados["forma_pagamento"]
                    venda.tipo_pagamento = dados["tipo_pagamento"]
                    venda.estado_transacao = dados["estado_transacao"]
                    venda.metodo_entrega = dados["metodo_entrega"]
                    venda.desconto = dados["desconto"]
                    venda.valor_total = dados["valor_total"]
                    venda.valor_entrega = dados["taxa_entrega"]
                    venda.valor_pago = dados["valor_pago"]
                    venda.troco = dados["troco"]
                    venda.descricao = dados["desc_venda"]
                    venda.cliente = dados["cliente"]
                    venda.usuario = dados["user"]
                    venda.loja = dados["loja"]
                    venda.save()
                    mensagem = "Venda atualizada com sucesso."
                except models.Venda.DoesNotExist:
                    # Se a venda não existir, podemos optar por criar uma nova ou lançar um erro
                    return None, "Venda não encontrada para atualização."
            else:  # Caso contrário, criamos uma nova venda
                venda = models.Venda.objects.create(
                    forma_pagamento=dados["forma_pagamento"],
                    tipo_pagamento=dados["tipo_pagamento"],
                    estado_transacao=dados["estado_transacao"],
                    metodo_entrega=dados["metodo_entrega"],
                    desconto=dados["desconto"],
                    valor_total=dados["valor_total"],
                    valor_entrega=dados["taxa_entrega"],
                    valor_pago=dados["valor_pago"],
                    troco=dados["troco"],
                    descricao=dados["desc_venda"],
                    cliente=dados["cliente"],
                    usuario=dados["user"],
                    loja=dados["loja"],
                )
                mensagem = "Venda criada com sucesso."

            return venda, mensagem
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
                        "valor_entrega": valor_entrega,
                        "time_pedido": timezone.now().time(),
                        "motoboy_id": id_motoboy,
                    },
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

    def _processar_dados_galoes(data, venda):
        try:
            # Iterar sobre as entradas do request.POST
            for _, troca in data.items():
                # Extrair os dados da troca
                data_entrada = {
                    "validade": troca.get("data_validade_entrada"),
                    "fabricacao": troca.get("data_fabricacao_entrada"),
                    "tipo": troca.get("tipo_entrada"),
                }

                data_saida = {
                    "validade": troca.get("data_validade_saida"),
                    "fabricacao": troca.get("data_fabricacao_saida"),
                    "tipo": troca.get("tipo_saida"),
                }

                descricao = troca.get("descricao_gestão_galao")

                # Verificar se os dados necessários estão presentes
                if all(
                    value != ""
                    for value in data_entrada.values() and data_saida.values()
                ):
                    # Criar ou atualizar o galão de entrada
                    galao_entrada, created_entrada = models.Galao.objects.get_or_create(
                        data_validade=data_entrada["validade"],
                        data_fabricacao=data_entrada["fabricacao"],
                        titulo=data_entrada["tipo"],
                        loja=venda.loja,
                    )

                    # Criar ou atualizar o galão de saída
                    galao_saida, created_saida = models.Galao.objects.get_or_create(
                        data_validade=data_saida["validade"],
                        data_fabricacao=data_saida["fabricacao"],
                        titulo=data_saida["tipo"],
                        loja=venda.loja,
                    )

                    # Atualizar as quantidades
                    galao_entrada.quantidade = (
                        1 if created_entrada else galao_entrada.quantidade + 1
                    )
                    galao_entrada.save()

                    galao_saida.quantidade = (
                        -1 if created_saida else galao_saida.quantidade - 1
                    )
                    galao_saida.save()

                    # Criar ou atualizar a gestão do galão
                    gestao_galao, _ = models.GestaoGalao.objects.update_or_create(
                        venda=venda,
                        defaults={
                            "galao_entrando": galao_entrada,
                            "galao_saiu": galao_saida,
                            "descricao": descricao,
                        },
                    )
            return True
        except Exception as e:
            # Tratar possíveis erros
            print(f"Erro ao processar dados dos galões: {e}")
            return False
