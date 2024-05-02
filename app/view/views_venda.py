from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..utils import utils
from ..static import Alerta, UserInfo
from ..models import (
    Venda,
    Associado,
    Produto,
    Loja,
    Cliente,
    ItemCompra,
    Galao,
    GestaoGalao,
)
from django.db.models import Q
from ..processos.venda import processos
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict


class views_venda:

    @staticmethod
    @utils.verificar_permissoes(codigo_model=7)
    def lista_vendas(request, context=None, id_loja=None):

        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = utils.criar_alerta_js(alerta)

        return render(request, "venda/lista_vendas.html", context)

    @csrf_exempt
    def obter_dados(request):
        if request.method == "GET":
            try:
                id_empresa = UserInfo.get_id_empresa(request, True)
                id_usuario = UserInfo.get_id_usuario(request)
                context = {}
                associacao = Associado.objects.filter(
                    usuario_id=id_usuario, status_acesso=True
                )
                ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

                produtos = Produto.objects.filter(
                    Q(loja_id__in=ids_lojas_associadas), loja__empresa_id=id_empresa
                )
                lojas = Loja.objects.filter(Q(id_loja__in=ids_lojas_associadas))

                vendas = Venda.objects.filter(
                    Q(loja_id__in=ids_lojas_associadas),
                    loja__empresa__id_empresa=id_empresa,
                ).prefetch_related("loja")
                context = {
                    "success": True,
                    "lojas": list(lojas.values()),
                    "produtos": list(produtos.values()),
                    "vendas": list(vendas.values()),
                }

                return JsonResponse(context)
            except Associado.DoesNotExist:
                context["menssage"] = (
                    "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
                )
            except Produto.DoesNotExist:
                context["menssage"] = (
                    "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
                )
        return JsonResponse(
            {
                "error": "erro, ao buscar dados..",
            },
            context,
            status=405,
        )

    def criar_venda(request):
        try:
            if request.method == "POST":
                return views_venda.insert_venda_ajax(request)
            else:
                return views_venda._open_venda(request)
        except Exception as e:
            mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)

    @csrf_exempt
    @utils.verificar_permissoes(codigo_model=7)
    def insert_venda_ajax(request):
        try:
            # Processa a venda
            id = UserInfo.get_id_usuario(request)
            venda, mensagem_erro = processos._processar_venda(request.POST, id)
            if venda is not None:
                if venda.metodo_entrega == "entrega_no_local":
                    id_motoboy = request.POST.get("motoboy", "").strip()
                    if id_motoboy != "0":
                        processos.processo_entrega(venda=venda, id_motoboy=id_motoboy)
                if venda.forma_pagamento == "dinheiro":
                    processos.processar_caixa(venda)
                # Processa o carrinho
                processos._processar_carrinho(request.POST, venda)
                # Processa os dados dos galões
                processos._processar_dados_galoes(request, venda)

                return JsonResponse({"success": True, "message": "venda processada."})
            elif mensagem_erro:
                return JsonResponse({"error": mensagem_erro})

        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"error": mensagem_erro}, status=500)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=7)
    def _open_venda(request):
        try:
            context = {}
            id_usuario = UserInfo.get_id_usuario(request)
            id_empresa = UserInfo.get_id_empresa(request)

            associacao = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            # Obtém uma lista de IDs de loja associadas
            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

            # Filtra os produtos com base nas lojas associadas
            produtos = Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas), loja__empresa_id=id_empresa
            )
            context = {
                "list_produtos": produtos,
                "open_modal": True,
            }
            return views_venda.lista_vendas(request, context)
        except Associado.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
            )
            context["open_modal"] = False
            return views_venda.lista_vendas(request, context)
        except Produto.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
            )
            context["open_modal"] = False
            return views_venda.lista_vendas(request, context)
        except Exception as e:
            mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=7)
    def editar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=7)
    def selecionar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @csrf_exempt
    def selecionar_produto_by_venda(request, id_venda):
        try:
            # Tenta encontrar a venda pelo ID
            itens_compra = ItemCompra.objects.filter(venda_id=id_venda)
            # Inicializa uma lista para armazenar os detalhes dos produtos
            detalhes_produtos = []
            # Itera sobre os itens de compra para obter os detalhes dos produtos
            for item in itens_compra:
                detalhes_produto = {
                    "id_produto": item.produto.id_produto,
                    "nome": item.produto.nome,
                    "preco_venda": item.produto.preco_venda,
                    "quantidade": item.quantidade,
                    "quantidade_atual_estoque": item.produto.quantidade_atual_estoque,
                    "fabricante": item.produto.fabricante,
                    "descricao": item.produto.descricao,
                    # Adicione mais campos do produto conforme necessário
                }
                detalhes_produtos.append(detalhes_produto)
            # Retorna os produtos como JSON
            return JsonResponse(
                {
                    "success": True,
                    "message": "Venda processada.",
                    "list_produtos": detalhes_produtos,
                }
            )
        except Venda.DoesNotExist:
            # Se a venda não for encontrada, retorna uma resposta de erro
            return JsonResponse({"message": "Venda não encontrada"}, status=404)
        except Exception as e:
            # Se ocorrer qualquer outro erro, retorna uma resposta de erro com a mensagem do erro
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @csrf_exempt
    def selecionar_retornaveis_by_venda(request, id_venda):
        try:
            gestao_galoes = GestaoGalao.objects.filter(venda__id_venda=id_venda)

            # Lista para armazenar os dados
            data_list = []

            # Itera sobre os objetos GestaoGalao
            for gestao_galao in gestao_galoes:
                gestao_galao_dict = model_to_dict(gestao_galao)

                # Verifica se é entrada ou saída
                if gestao_galao.galao_entrando:
                    galao = gestao_galao.galao_entrando
                    gestao_galao_dict["tipo"] = "entrada"
                elif gestao_galao.galao_saiu:
                    galao = gestao_galao.galao_saiu
                    gestao_galao_dict["tipo"] = "saida"
                else:
                    # Caso contrário, ignora este GestaoGalao
                    continue

                # Adiciona os dados do galão ao dicionário
                galao_dict = model_to_dict(galao)
                gestao_galao_dict.update(galao_dict)

                data_list.append(gestao_galao_dict)

            # Retorna os produtos como JSON
            return JsonResponse(
                {
                    "success": True,
                    "message": "Venda processada.",
                    "list_retornaveis": data_list,
                }
            )
        except Venda.DoesNotExist:
            # Se a venda não for encontrada, retorna uma resposta de erro
            return JsonResponse({"message": "Venda não encontrada"}, status=404)
        except Exception as e:
            # Se ocorrer qualquer outro erro, retorna uma resposta de erro com a mensagem do erro
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @csrf_exempt
    def selecionar_cliente_by_venda(request, id_venda):
        try:
            # Obtém a venda junto com o cliente e suas informações de endereço relacionadas
            venda = Venda.objects.select_related("cliente", "cliente__endereco").get(
                id_venda=id_venda
            )

            # Agora você pode acessar o cliente e seu endereço diretamente sem fazer consultas adicionais
            cliente = venda.cliente
            if cliente:
                # Construir o dicionário de dados do cliente e sua última venda
                data = {
                    "id_cliente": (cliente.id_cliente),
                    "nome": cliente.nome_cliente,
                    "telefone": cliente.telefone_cliente,
                    "descricao": cliente.descricao_cliente,
                    "tipo_cliente": cliente.tipo_cliente,
                    "rua": cliente.endereco.rua if cliente.endereco else None,
                    "numero": (cliente.endereco.numero if cliente.endereco else None),
                    "cep": (
                        cliente.endereco.codigo_postal if cliente.endereco else None
                    ),
                    "estado": (cliente.endereco.estado if cliente.endereco else None),
                    "bairro": (cliente.endereco.bairro if cliente.endereco else None),
                    "cidade": (cliente.endereco.cidade if cliente.endereco else None),
                    "descricao": (
                        cliente.endereco.descricao if cliente.endereco else None
                    ),
                }
                return JsonResponse(
                    {"success": True, "message": "Venda processada.", "cliente": data}
                )
            return JsonResponse(
                {
                    "success": False,
                    "message": "não há cliente associado a essa venda",
                    "cliente": None,
                }
            )

        except Venda.DoesNotExist:
            return JsonResponse({"message": "Venda não encontrada"}, status=404)

        except Cliente.DoesNotExist:
            return JsonResponse({"message": "cliente não encontrada"}, status=404)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=7)
    def excluir_venda(request, venda_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para excluir a venda com id=venda_id
            return HttpResponse(f"Excluindo a venda {venda_id}")
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )
