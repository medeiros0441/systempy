from django.shortcuts import render
from django.http import HttpResponse
from ..def_global import erro


# Vendas
def lista_vendas(request):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para listar as vendas
        return HttpResponse("Lista de vendas")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def editar_venda(request, venda_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para editar a venda com id=venda_id
        return HttpResponse(f"Editando a venda {venda_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def selecionar_venda(request, venda_id):
    if (
        request.session.get("id_empresa", 0) != 0
        and request.session.get("id_usuario", 0) != 0
        and request.session.get("status_acesso", "") == "ativo"
    ):
        # Lógica para selecionar a venda com id=venda_id
        return HttpResponse(f"Selecionando a venda {venda_id}")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


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
