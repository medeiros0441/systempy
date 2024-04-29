from django.shortcuts import render, redirect
from ..utils import utils
from django.http import HttpResponse
from ..static import Alerta, UserInfo
from ..models import Loja, Produto
from ..forms.form_produto import ProdutoForm as Form
import datetime

class views_produto:
    @staticmethod
    @utils.verificar_permissoes(6)
    def lista_produtos(request, context=None):
        id_empresa = UserInfo.get_id_empresa(request, True)
        if context is None:
            context = {}
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = utils.criar_alerta_js(alerta)

        try:
            produtos = Produto.objects.filter(loja__empresa__id_empresa=id_empresa)
            context["produtos"] = produtos
        except Produto.DoesNotExist:
            pass
        return render(request, "produto/lista_produtos.html", context)

    @staticmethod
    @utils.verificar_permissoes(6)
    def criar_produto(request):
        try:
            if request.method == "POST":
                status, obj = views_produto.validate_form(request.POST)
                if status:
                    produto = Produto(**obj)  # Cria uma instância do Produto
                    produto.save()  # Salvando o produto no banco de dados
                    Alerta.set_mensagem("Cadastrado com Sucesso.")
                    return redirect("lista_produtos")
                else:
                    Alerta.set_mensagem(mensagem_erro)
                    return views_produto.lista_produtos(
                        request,
                        {"open_modal": True, "form_produto": True},
                    )
            else:
                return views_produto.lista_produtos(
                    request,
                    {"open_modal": True, "form_produto": True},
                )
        except Exception as e:
            mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)

    def validate_form(form_data):
        loja = form_data.get('loja')
        nome = form_data.get('nome', '')
        quantidade_atual_estoque = form_data.get('quantidade_atual_estoque', '')
        quantidade_minima_estoque = form_data.get('quantidade_minima_estoque', '')
        is_retornavel = form_data.get('is_retornavel', '')
        data_validade = form_data.get('data_validade', '')
        preco_compra = form_data.get('preco_compra', '')
        preco_venda = form_data.get('preco_venda', '')
        fabricante = form_data.get('fabricante', '')
        descricao = form_data.get('descricao', '')

        # Validando os campos
        if loja == "0":
            return False, "Selecione uma loja."

        if not nome:
            return False, "O nome do produto é obrigatório."

        try:
            quantidade_atual_estoque = int(quantidade_atual_estoque)
            if quantidade_atual_estoque < 0:
                raise ValueError
        except ValueError:
            return False, "A quantidade atual em estoque deve ser um número inteiro positivo."

        try:
            quantidade_minima_estoque = int(quantidade_minima_estoque)
            if quantidade_minima_estoque < 0:
                raise ValueError
        except ValueError:
            return False, "A quantidade mínima em estoque deve ser um número inteiro positivo."

        if is_retornavel not in ['0', '1']:
            return False, "Selecione se o produto é retornável."

        if data_validade:
            try:
                datetime.datetime.strptime(data_validade,'%Y-%m-%d')
            except ValueError:
                return False, "A data de validade deve estar no formato YYYY-MM-DD."

        try:
            preco_compra = float(preco_compra)
            if preco_compra < 0:
                raise ValueError
        except ValueError:
            return False, "O preço de compra deve ser um número positivo."

        try:
            preco_venda = float(preco_venda)
            if preco_venda < 0:
                raise ValueError
        except ValueError:
            return False, "O preço de venda deve ser um número positivo."

        if not fabricante:
            return False, "O fabricante é obrigatório."

        if not descricao:
            return False, "A descrição é obrigatória."

        produto = Produto(
            loja=loja,
            nome=nome,
            quantidade_atual_estoque=quantidade_atual_estoque,
            quantidade_minima_estoque=quantidade_minima_estoque,
            is_retornavel=bool(int(is_retornavel)),
            data_validade=data_validade,
            preco_compra=preco_compra,
            preco_venda=preco_venda,
            fabricante=fabricante,
            descricao=descricao
        )

        return True, produto
    @staticmethod
    @utils.verificar_permissoes(6)
    def editar_produto(request, id_produto):
        try:
            id_empresa = UserInfo.get_id_empresa(request)
            produto = Produto.objects.filter(
                id_produto=id_produto, loja__empresa_id=id_empresa
            ).first()

            if not produto:
                return utils.erro(
                    request, "Você não tem permissão para acessar o produto"
                )

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
            return utils.erro(request, mensagem_erro)

 
    @staticmethod
    @utils.verificar_permissoes(6)
    def acrescentar_produto(request):
        try:

            id_empresa = UserInfo.get_id_empresa(request, True)
            produtos = Produto.objects.filter(loja__empresa__id_empresa=id_empresa)
            for produto in produtos:
                if produto.loja.empresa.id_empresa != id_empresa:
                    return utils.erro(
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
                    return utils.erro(
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
            return utils.erro(request, mensagem_erro)

    @staticmethod
    @utils.verificar_permissoes(6)
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
            return utils.erro(request, mensagem_erro)

    @staticmethod
    @utils.verificar_permissoes(6)
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
            return utils.erro(request, mensagem_erro)
