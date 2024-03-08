from django.shortcuts import render, redirect
from ..def_global import criar_alerta_js, erro
from django.http import HttpResponse
from ..static import Alerta, UserInfo
from ..models.produto import Produto
from ..forms.form_produto import ProdutoForm as Form


def lista_produtos(request, context=None):
    id_empresa = UserInfo.get_id_empresa(request, True)
    if context is None:
        context = {}
    alerta = Alerta.get_mensagem()
    if alerta:
        context["alerta_js"] = criar_alerta_js(alerta)

    try:
        produtos = Produto.objects.filter(loja__empresa__id_empresa=id_empresa)
        context["produtos"] = produtos
    except Produto.DoesNotExist:
        pass
    return render(request, "produto/lista_produtos.html", context)


def criar_produto(request):
    try:
        if request.method == "POST":
            form_produto = Form(request.POST, request=request)

            if form_produto.is_valid():
                form_produto.save()  # Cria um novo registro de Loja
                Alerta.set_mensagem("Cadastrado com Sucesso.")
                return redirect("lista_produtos")
            else:
                if not form_produto.is_valid():
                    Alerta.set_mensagem("Formulário inválido.")
                # Renderiza o template com os formulários inválidos
                return lista_produtos(
                    request,
                    {
                        "open_modal": True,
                        "form_produto": form_produto,
                    },
                )
        else:
            form = Form(request=request)
            return lista_produtos(
                request,
                {"open_modal": True, "form_produto": form},
            )
    except Exception as e:
        mensagem_erro = str(e)
        return erro(request, mensagem_erro)


def editar_produto(request, id_produto):
    try:
        # Obter o produto existente pelo ID
        produto = Produto.objects.get(id_produto=id_produto)

        if request.method == "POST":
            form_produto = Form(request.POST, instance=produto, request=request)

            if form_produto.is_valid():
                form_produto.save()  # Atualiza o registro do produto
                Alerta.set_mensagem("Produto atualizado com sucesso.")
                return redirect("lista_produtos")
            else:
                if not form_produto.is_valid():
                    Alerta.set_mensagem("Formulário inválido.")
                # Renderiza o template com os formulários inválidos
                return lista_produtos(
                    request,
                    {
                        "open_modal": True,
                        "form_produto": form_produto,
                    },
                )
        else:
            form_produto = Form(instance=produto, request=request)
            return lista_produtos(
                request,
                {"open_modal": True, "form_produto": form_produto},
            )
    except Produto.DoesNotExist:
        Alerta.set_mensagem("Produto não encontrado.")
        return redirect("lista_produtos")
    except Exception as e:
        mensagem_erro = str(e)
        return erro(request, mensagem_erro)


def selecionar_produto(request, produto_id):

    return False


def excluir_produto(request, id_produto):
    try:
        produto = Produto.objects.get(id_produto=id_produto)
        if produto:
            produto.delete()
            Alerta.set_mensagem("Produto excluído com sucesso.")
            return redirect("lista_produtos")
    except Produto.DoesNotExist:
        Alerta.set_mensagem("Produto não encontrado.")
        return redirect("lista_produtos")
    except Exception as e:
        mensagem_erro = str(e)
        return erro(request, mensagem_erro)