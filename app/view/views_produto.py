from django.shortcuts import render, redirect
from ..def_global import criar_alerta_js, erro, verificar_permissoes
from django.http import HttpResponse
from ..static import Alerta, UserInfo
from ..models import Loja, Produto
from ..forms.form_produto import ProdutoForm as Form


class views_produto:
    @staticmethod
    @verificar_permissoes(6)
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

    @staticmethod
    @verificar_permissoes(6)
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
                    return views_produto.lista_produtos(
                        request,
                        {
                            "open_modal": True,
                            "form_produto": form_produto,
                        },
                    )
            else:
                form = Form(request=request)
                return views_produto.lista_produtos(
                    request,
                    {"open_modal": True, "form_produto": form},
                )
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(6)
    def editar_produto(request, id_produto):
        try:
            id_empresa = UserInfo.get_id_empresa(request)
            produto = Produto.objects.filter(
                id_produto=id_produto, loja__empresa_id=id_empresa
            ).first()

            if not produto:
                return erro(request, "Você não tem permissão para acessar o produto")

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
                    return views_produto.lista_produtos(
                        request,
                        {
                            "open_modal": True,
                            "form_produto": form_produto,
                        },
                    )
            else:
                form_produto = Form(instance=produto, request=request)
                return views_produto.lista_produtos(
                    request,
                    {"open_modal": True, "form_produto": form_produto},
                )
        except Produto.DoesNotExist:
            Alerta.set_mensagem("Produto não encontrado.")
            return redirect("lista_produtos")
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(6)
    def acrescentar_produto(request):
        try:

            id_empresa = UserInfo.get_id_empresa(request, True)
            produtos = Produto.objects.filter(loja__empresa__id_empresa=id_empresa)
            for produto in produtos:
                if produto.loja.empresa.id_empresa != id_empresa:
                    return erro(
                        request, "Você não tem permissão para acessar este produto"
                    )

            if request.method == "POST":
                # Obtém os dados do formulário
                id_produto = request.POST.get("id_produto")
                id_loja = request.POST.get("id_loja")
                quantidade_acrescentar = int(
                    request.POST.get("id_quantidade_acrescentar")
                )

                # Verifica se os valores são válidos
                if not id_produto or not id_loja or quantidade_acrescentar < 0:
                    Alerta.set_mensagem("Valores inválidos fornecidos no formulário")
                    loja_list = Loja.objects.filter(empresa__id_empresa=id_empresa)
                    return views_produto.lista_produtos(
                        request,
                        {
                            "open_modal": True,
                            "produtos_list": produtos,
                            "lojas": loja_list,
                        },
                    )

                produto = Produto.objects.get(id_produto=id_produto)
                if produto.loja.empresa.id_empresa != id_empresa:
                    return erro(
                        request, "Você não tem permissão para acessar este produto"
                    )
                produto.quantidade_atual_estoque += quantidade_acrescentar
                produto.save()
                Alerta.set_mensagem("Produto acrescentado com sucesso.")
                loja_list = Loja.objects.filter(empresa__id_empresa=id_empresa)
                return redirect("acrescentar_produto")
            else:

                loja_list = Loja.objects.filter(empresa__id_empresa=id_empresa)
                return views_produto.lista_produtos(
                    request,
                    {"open_modal": True, "produtos_list": produtos, "lojas": loja_list},
                )
        except Produto.DoesNotExist:
            Alerta.set_mensagem("Produtos não encontrado.")
            return redirect("lista_produtos")
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(6)
    def selecionar_produto(request, id_produto):
        try:
            produto = Produto.objects.get(id_produto=id_produto)
            if produto:
                return views_produto.lista_produtos(
                    request,
                    {"open_modal": True, "text_produto": produto},
                )
        except Produto.DoesNotExist:
            Alerta.set_mensagem("Produto não encontrado.")
            return redirect("lista_produtos")
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(6)
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
