from django.shortcuts import render
from django.http import HttpResponse
from ..def_global import erro


def lista_produtos(request):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para listar os produtos
        return HttpResponse("Lista de produtos")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def editar_produto(request, produto_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para editar o produto com id=produto_id
        return HttpResponse(f"Editando o produto {produto_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def selecionar_produto(request, produto_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para selecionar o produto com id=produto_id
        return HttpResponse(f"Selecionando o produto {produto_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def excluir_produto(request, produto_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para excluir o produto com id=produto_id
        return HttpResponse(f"Excluindo o produto {produto_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")
