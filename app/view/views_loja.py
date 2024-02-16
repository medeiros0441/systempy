from django.shortcuts import render
from django.http import HttpResponse
from ..def_global import erro


from ..models.produto import Loja, Produto


def lista_lojas(request):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para listar as lojas
        return HttpResponse("Lista de lojas")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def editar_loja(request, loja_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para editar a loja com id=loja_id
        return HttpResponse(f"Editando a loja {loja_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def selecionar_loja(request, loja_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para selecionar a loja com id=loja_id
        return HttpResponse(f"Selecionando a loja {loja_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def excluir_loja(request, loja_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para excluir a loja com id=loja_id
        return HttpResponse(f"Excluindo a loja {loja_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")
