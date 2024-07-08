from django.shortcuts import render, redirect
from app.utils import Utils
from django.http import HttpResponse
from app.static import Alerta, UserInfo
from ..models import Loja, Produto
import datetime
from decimal import Decimal
from django.utils import timezone

from .views_erro import views_erro


class views_produto:
    @staticmethod
    @Utils.verificar_permissoes(6, True)
    def lista_produtos(request, context=None):
        id_empresa = UserInfo.get_id_empresa(request, True)
        if context is None:
            context = {}
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = Utils.criar_alerta_js(alerta)

        try:
            produtos = Produto.objects.filter(
                loja__empresa__id_empresa=id_empresa, status=True
            )
            context["produtos"] = produtos
        except Produto.DoesNotExist:
            pass
        return render(request, "produto/lista_produtos.html", context)

    @staticmethod
    @Utils.verificar_permissoes(6, True)
    def form_produto(request, id_produto=None):
        try:
            produto = None

            if id_produto is not None:
                produto = Produto.objects.get(id_produto=id_produto)

            if request.method == "POST" or request.method == "PUT":
                status, mensagem, data = views_produto.validate_form(request.POST)
                if status:
                    if id_produto is None:
                        produto = (
                            Produto()
                        )  # Criar um novo produto apenas se id_produto for None
                    else:
                        produto = Produto.objects.get(
                            id_produto=id_produto
                        )  # Buscar o produto existente

                    # Atribuir os valores aos campos do produto
                    produto.loja_id = int(data["loja"])
                    produto.nome = data["nome"]
                    produto.quantidade_atual_estoque = data["quantidade_atual_estoque"]
                    produto.quantidade_minima_estoque = data[
                        "quantidade_minima_estoque"
                    ]
                    produto.is_retornavel = bool(int(data["is_retornavel"]))
                    produto.data_validade = data["data_validade"]
                    produto.preco_compra = data["preco_compra"]
                    produto.preco_venda = data["preco_venda"]
                    produto.fabricante = data["fabricante"]
                    produto.descricao = data["descricao"]

                    produto.save()  # Salvando o produto no banco de dados

                    if id_produto is None:
                        Alerta.set_mensagem("Cadastrado com Sucesso.")
                    else:
                        Alerta.set_mensagem("Editado com Sucesso.")

                    return redirect("lista_produtos")
                else:
                    Alerta.set_mensagem(mensagem)
                    return views_produto.lista_produtos(
                        request, {"open_modal": True, "form_produto": data}
                    )
            else:
                if produto is None:
                    produto = True
                return views_produto.lista_produtos(
                    request,
                    {"open_modal": True, "form_produto": produto},
                )
        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)

    def validate_form(form_data):
        data = {
            "loja": form_data.get("select_loja"),
            "nome": form_data.get("nome", ""),
            "quantidade_atual_estoque": form_data.get("quantidade_atual_estoque", ""),
            "quantidade_minima_estoque": form_data.get("quantidade_minima_estoque", ""),
            "is_retornavel": form_data.get("is_retornavel", ""),
            "data_validade": form_data.get("data_validade", ""),
            "preco_compra": form_data.get("preco_compra", ""),
            "preco_venda": form_data.get("preco_venda", ""),
            "fabricante": form_data.get("fabricante", ""),
            "descricao": form_data.get("descricao", ""),
        }

        # Validando os campos
        if data["loja"] == "0" or data["loja"] is None:
            return False, "Selecione uma loja.", data

        if not data["nome"]:
            return False, "O nome do produto é obrigatório.", data

        try:
            data["quantidade_atual_estoque"] = int(data["quantidade_atual_estoque"])
            if data["quantidade_atual_estoque"] < 0:
                raise ValueError
        except ValueError:
            return (
                False,
                "A quantidade atual em estoque deve ser um número inteiro positivo.",
                data,
            )

        try:
            data["quantidade_minima_estoque"] = int(data["quantidade_minima_estoque"])
            if data["quantidade_minima_estoque"] < 0:
                raise ValueError
        except ValueError:
            return (
                False,
                "A quantidade mínima em estoque deve ser um número inteiro positivo.",
                data,
            )

        if data["is_retornavel"] not in ["0", "1"]:
            return False, "Selecione se o produto é retornável.", data

        try:
            data["preco_compra"] = Decimal(data["preco_compra"].replace(",", "."))
            if data["preco_compra"] < 0:
                raise ValueError
        except ValueError:
            return False, "O preço de compra deve ser um número positivo.", data

        try:
            data["preco_venda"] = Decimal(data["preco_venda"].replace(",", "."))
            if data["preco_venda"] < 0:
                raise ValueError
        except ValueError:
            return False, "O preço de venda deve ser um número positivo.", data

        if not data["fabricante"]:
            return False, "O fabricante é obrigatório.", data

        return True, None, data

    @staticmethod
    @Utils.verificar_permissoes(6, True)
    def acrescentar_produto(request):
        try:

            id_empresa = UserInfo.get_id_empresa(request, True)
            produtos = Produto.objects.filter(
                loja__empresa__id_empresa=id_empresa, status=True
            )
            for produto in produtos:
                if produto.loja.empresa.id_empresa != id_empresa:
                    return views_erro.erro(
                        request,
                        request,
                        "Você não tem permissão para acessar este produto",
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
                    return views_erro.erro(
                        request,
                        request,
                        "Você não tem permissão para acessar este produto",
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
            return views_erro.erro(request, mensagem_erro)

    @staticmethod
    @Utils.verificar_permissoes(6, True)
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
            return views_erro.erro(request, mensagem_erro)

    @staticmethod
    @Utils.verificar_permissoes(6, True)
    def excluir_produto(request, id_produto):
        try:
            produto = Produto.objects.get(id_produto=id_produto)
            if produto:
                produto.status = False
                produto.save()
                Alerta.set_mensagem("Produto excluído com sucesso.")
                return redirect("lista_produtos")
        except Produto.DoesNotExist:
            Alerta.set_mensagem("Produto não encontrado.")
            return redirect("lista_produtos")
        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)
