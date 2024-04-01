from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..def_global import erro, criar_alerta_js
from ..static import Alerta, UserInfo
from ..models import Venda, Configuracao, Usuario, Associado, Loja, Cliente, Produto,ItemCompra,Compra
from functools import wraps
from ..forms import VendaForm, ClienteForm, EnderecoForm
from django.db.models import Q


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
            if request.method == "POST":
                return view_vendas._insert_venda(request)
            else:
                return view_vendas._open_venda(request)
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    def _insert_venda(request):
        try:
            
            for item_carrinho in request.POST.getlist("item_carrinho"):
                id_produto, quantidade = item_carrinho.split("|")
                produto = produto.object.filter(id_produto= id_produto)
                ItemCompra.produto = produto 
                ItemCompra.quantidade = quantidade 
                ItemCompra.preco_unitario = produto.preco_venda
                
            id_usuario = UserInfo.get_id_usuario(request)
            tipo_cliente =  request.POST.get("tipo_cliente")
            if tipo_cliente == 1:
                form_cliente = ClienteForm(request.POST)
            elif tipo_cliente == 2:
                form_cliente = ClienteForm(request.POST)
                form_endereco = EnderecoForm(request.POST)
                
            form_venda = VendaForm(id_usuario, request.POST)
            venda = form_venda.save(commit=False)
             

            if (
                form_venda.is_valid()
                and form_cliente.is_valid()
                and form_endereco.is_valid()
            ):
                # Recuperar os dados dos formulários
                dados_venda = form_venda.cleaned_data
                dados_cliente = form_cliente.cleaned_data
                dados_endereco = form_endereco.cleaned_data
                # Aqui você pode criar instâncias dos modelos correspondentes e salvar no banco de dados
                venda = form_venda.save(
                    commit=False
                )  # Se precisar de lógica adicional antes de salvar
                cliente = form_cliente.save(commit=False)
                endereco = form_endereco.save(commit=False)
                venda.cliente = cliente
                venda.endereco = endereco
                venda.save()

            else:
                form_venda = VendaForm()
                form_cliente = ClienteForm()
                form_endereco = EnderecoForm()
            return ""
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    def _open_venda(request):
        try:
            context = {}
            id_usuario = UserInfo.get_id_usuario(request)
            id_empresa = UserInfo.get_id_empresa(request)
            # Obter todas as associações do usuário com status de acesso verdadeiro
            associacao = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            # Obter os clientes da empresa
            clientes = Cliente.objects.filter(empresa_id=id_empresa)

            # Obtém uma lista de IDs de loja associadas
            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

            # Filtra os produtos com base nas lojas associadas
            produtos = Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas), loja__empresa_id=id_empresa
            )

            # Inicializar os formulários
            form_venda = VendaForm(id_usuario)
            form_cliente = ClienteForm()
            form_endereco = EnderecoForm()
            # Criar o contexto
            context = {
                "list_clientes": clientes,
                "form_cliente": form_cliente,
                "form_venda": form_venda,
                "form_endereco": form_endereco,
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
