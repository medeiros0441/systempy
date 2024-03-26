from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..def_global import erro, criar_alerta_js
from ..static import Alerta, UserInfo
from ..models import Venda, Configuracao, Usuario, Associado, Loja, Cliente,Produto
from functools import wraps
from ..forms import VendaForm, ClienteForm


def verificar_permissoes(codigo_model):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            id_usuario = UserInfo.get_id_usuario(request)
            try:
                configuracao = Configuracao.objects.get(
                    usuario_id=id_usuario, codigo=codigo_model
                )
                if configuracao.status_acesso == False:
                    Alerta.set_mensagem(
                        "Acesso negado: você não tem permissão para executar o método."
                    )
                    return erro(
                        request,
                        "Acesso negado: você não tem permissão para executar o método.",
                    )
            except Configuracao.DoesNotExist:
                Alerta.set_mensagem("Configuração não encontrada.")
                return erro(request, "Configuração não encontrada.")
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class view_vendas:

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def lista_vendas(request, context=None, id_loja=None):

        id_empresa = UserInfo.get_id_empresa(request, True)
        if context is None:
            context = {}
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = criar_alerta_js(alerta)

        try:
            if id_loja is None:
                vendas = Venda.objects.filter(loja__empresa__id_empresa=id_empresa)
            else:
                vendas = Venda.objects.filter(
                    loja__empresa__id_empresa=id_empresa, loja_id_loja=id_loja
                )
            context["vendas"] = vendas
        except Venda.DoesNotExist:
            pass
        return render(request, "venda/lista_vendas.html", context)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def criar_venda(request):
        try:
            context = {}
            id_usuario = UserInfo.get_id_usuario(request)
            id_empresa = UserInfo.get_id_empresa(request)
            # Obter todas as associações do usuário com status de acesso verdadeiro
            Associado.objects.filter(usuario_id=id_usuario, status_acesso=True)
            # Obter os clientes da empresa
            clientes = Cliente.objects.filter(empresa_id=id_empresa)
            produtos = Produto.objects.filter(loja__empresa__id_empresa=id_empresa)

            # Inicializar os formulários
            form_venda = VendaForm(id_usuario)
            form_cliente = ClienteForm()
              # Criar o contexto
            context = {
                "list_clientes": clientes,
                "form_cliente": form_cliente,
                "form_venda": form_venda,
                "list_produtos": produtos,
                "open_modal": True,
            }
            return view_vendas.lista_vendas(request, context)
        except Associado.DoesNotExist:
            Alerta.set_mensagem(
                    "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
                )
            context["open_modal"] = False
            return view_vendas.lista_vendas(request, context)
        except Produto.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
            )
            context["open_modal"] = False
            return view_vendas.lista_vendas(request, context)
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def editar_venda(request, venda_id):

        return view_vendas.lista_vendas(request)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def selecionar_venda(request, venda_id):

        return view_vendas.lista_vendas(request)

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
