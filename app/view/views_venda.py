from django.shortcuts import render
from django.http import HttpResponse
from ..def_global import erro
from ..static import Alerta, UserInfo
from django.shortcuts import render, redirect
from ..def_global import criar_alerta_js, erro
from ..models import Venda


def lista_vendas(request, context=None, id_loja=0):

    id_empresa = UserInfo.get_id_empresa(request, True)
    if context is None:
        context = {}
    alerta = Alerta.get_mensagem()
    if alerta:
        context["alerta_js"] = criar_alerta_js(alerta)

    try:
        produtos = Vendas.objects.filter(loja__empresa__id_empresa=id_empresa)
        context["produtos"] = produtos
    except Produto.DoesNotExist:
        pass
    return render(request, "produto/lista_produtos.html", context)


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
