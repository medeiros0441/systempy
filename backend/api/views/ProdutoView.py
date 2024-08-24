from django.shortcuts import render, redirect
from api.user import UserInfo
from api.models import LojaModel, ProdutoModel
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from api.permissions import permissions, CustomPermission
from rest_framework import viewsets, status


class ProdutoView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="produto", auth_required=True)]

    @staticmethod
    @require_http_methods(["POST", "PUT"])
    @permissions.isAutorizado(6, True)
    def form_produto(request, id_produto=None):
        try:
            data = json.loads(
                request.body
            )  # Carrega e decodifica os dados JSON do corpo da requisição
            produto = None

            if id_produto is not None:
                produto = get_object_or_404(ProdutoModel, id_produto=id_produto)

            status, mensagem, data = ProdutoView.validate_form(data)
            if status:
                if id_produto is None:
                    produto = (
                        ProdutoModel()
                    )  # Criar um novo produto apenas se id_produto for None
                else:
                    produto = get_object_or_404(
                        ProdutoModel, id_produto=id_produto
                    )  # Buscar o produto existente

                # Atribuir os valores aos campos do produto
                produto.loja_id = int(data["loja"])
                produto.nome = data["nome"]
                produto.quantidade_atual_estoque = data["quantidade_atual_estoque"]
                produto.quantidade_minima_estoque = data["quantidade_minima_estoque"]
                produto.is_retornavel = bool(int(data["is_retornavel"]))
                produto.data_validade = data["data_validade"]
                produto.preco_compra = data["preco_compra"]
                produto.preco_venda = data["preco_venda"]
                produto.fabricante = data["fabricante"]
                produto.descricao = data["descricao"]

                produto.save()  # Salvando o produto no banco de dados

                mensagem_sucesso = (
                    "Cadastrado com Sucesso."
                    if id_produto is None
                    else "Editado com Sucesso."
                )
                return JsonResponse({"message": mensagem_sucesso}, status=200)
            else:
                return JsonResponse({"message": mensagem}, status=400)

        except ProdutoModel.DoesNotExist:
            return JsonResponse({"message": "ProdutoModel não encontrado."}, status=404)

        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @staticmethod
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
    @require_http_methods(["POST"])
    @permissions.isAutorizado(6, True)
    def acrescentar_produto(request):
        try:
            data = json.loads(
                request.body
            )  # Carrega e decodifica os dados JSON do corpo da requisição
            id_empresa = UserInfo.get_id_empresa(request, True)
            produtos = ProdutoModel.objects.filter(
                loja__empresa__id_empresa=id_empresa, status=True
            )

            for produto in produtos:
                if produto.loja.empresa.id_empresa != id_empresa:
                    return JsonResponse(
                        {"message": "Você não tem permissão para acessar este produto"},
                        status=403,
                    )

            # Obtém os dados do JSON
            id_produto = data.get("id_produto")
            id_loja = data.get("id_loja")
            quantidade_acrescentar = data.get("quantidade_acrescentar", 0)

            # Verifica se os valores são válidos
            if not id_produto or not id_loja or quantidade_acrescentar < 0:
                return JsonResponse(
                    {"message": "Valores inválidos fornecidos"},
                    status=400,
                )

            produto = ProdutoModel.objects.get(id_produto=id_produto)
            if produto.loja.empresa.id_empresa != id_empresa:
                return JsonResponse(
                    {"message": "Você não tem permissão para acessar este produto"},
                    status=403,
                )

            produto.quantidade_atual_estoque += quantidade_acrescentar
            produto.save()
            return JsonResponse(
                {"message": "ProdutoModel acrescentado com sucesso."}, status=200
            )

        except ProdutoModel.DoesNotExist:
            return JsonResponse({"message": "ProdutoModel não encontrado."}, status=404)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @staticmethod
    @require_http_methods(["GET"])
    @permissions.isAutorizado(6, True)
    def selecionar_produto(request, id_produto):
        try:
            produto = ProdutoModel.objects.get(id_produto=id_produto)
            return JsonResponse(
                {
                    "produto": {
                        "id_produto": produto.id_produto,
                        "nome": produto.nome,
                        "quantidade_atual_estoque": produto.quantidade_atual_estoque,
                        "quantidade_minima_estoque": produto.quantidade_minima_estoque,
                        "preco_compra": produto.preco_compra,
                        "preco_venda": produto.preco_venda,
                        "fabricante": produto.fabricante,
                        "descricao": produto.descricao,
                    }
                },
                status=200,
            )
        except ProdutoModel.DoesNotExist:
            return JsonResponse({"message": "ProdutoModel não encontrado."}, status=404)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @staticmethod
    @require_http_methods(["DELETE"])
    @permissions.isAutorizado(6, True)
    def excluir_produto(request, id_produto):
        try:
            produto = ProdutoModel.objects.get(id_produto=id_produto)
            produto.status = False
            produto.save()
            return JsonResponse(
                {"message": "ProdutoModel excluído com sucesso."}, status=200
            )
        except ProdutoModel.DoesNotExist:
            return JsonResponse({"message": "ProdutoModel não encontrado."}, status=404)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)
