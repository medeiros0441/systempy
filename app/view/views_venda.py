from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..def_global import erro, criar_alerta_js, verificar_permissoes
from ..static import Alerta, UserInfo
from ..models import Venda, Associado, Produto,Loja
from django.db.models import Q
from ..processos.venda import processos
from django.http import JsonResponse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


class views_venda:

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def lista_vendas(request, context=None, id_loja=None):
         
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = criar_alerta_js(alerta)

        return render(request, "venda/lista_vendas.html", context)

    @csrf_exempt
    def obter_dados(request):
        if request.method == 'POST':
            id_empresa = UserInfo.get_id_empresa(request, True)
            id_usuario = UserInfo.get_id_usuario(request)

            associacao = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

            produtos = Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas), loja__empresa_id=id_empresa
            )

            vendas = Venda.objects.filter(
                Q(loja_id__in=ids_lojas_associadas), loja__empresa__id_empresa=id_empresa
            )
            lojas = Loja.objects.filter(Q(id_loja__in=ids_lojas_associadas))
            dados = {
                "sucess":True,
                "lojas": list(lojas.values()),
                "produtos": list(produtos.values()),
                "vendas": list(vendas.values())
            }

            return JsonResponse(dados)

        return JsonResponse({"error": "Método não permitido"}, status=405)

    def criar_venda(request):
        try:
            if request.method == "POST":
                return views_venda.insert_venda_ajax(request)
            else:
                return views_venda._open_venda(request)
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @verificar_permissoes(codigo_model=7)
    @csrf_exempt
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
                return JsonResponse({"success": False, "error": mensagem_erro})

        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"success": False, "error": mensagem_erro}, status=500)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
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
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def editar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def selecionar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def excluir_venda(request, venda_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para excluir a venda com id=venda_id
            return HttpResponse(f"Excluindo a venda {venda_id}")
        else:
            return erro(request, "Você não está autorizado a fazer esta requisição.")
