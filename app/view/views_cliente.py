from django.shortcuts import render, get_object_or_404, redirect
from ..def_global import criar_alerta_js, erro, get_status
from django.shortcuts import render
from django.http import HttpResponse

from ..models.usuario import Usuario
from ..models.cliente import Cliente


def lista_clientes(request):

    if get_status(request):
        clientes = Cliente.objects.all()
        return render(request, "cliente/lista_clientes.html", {"clientes": clientes})
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def criar_cliente(request):
    if get_status(request):
        if request.method == "POST":
            nome_cliente = request.POST.get("nome_cliente")
            telefone = request.POST.get("telefone")
            ultima_compra = request.POST.get("ultima_compra")
            tipo_cliente = request.POST.get("tipo_cliente")

            cliente = Cliente.objects.create(
                nome_cliente=nome_cliente,
                telefone=telefone,
                ultima_compra=ultima_compra,
                tipo_cliente=tipo_cliente,
            )
            cliente.save()
            return redirect("cliente/lista_clientes")

        else:
            return render(request, "cadastrar_cliente.html")
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def editar_cliente(request, cliente_id):
    if get_status(request):
        cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
        if request.method == "POST":
            cliente.nome_cliente = request.POST.get("nome_cliente")
            cliente.telefone = request.POST.get("telefone")
            cliente.ultima_compra = request.POST.get("ultima_compra")
            cliente.tipo_cliente = request.POST.get("tipo_cliente")

            cliente.save()
            return redirect("cliente/lista_clientes")
        else:
            return render(request, "editar_cliente.html", {"cliente": cliente})
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def selecionar_cliente(request, cliente_id):
    if get_status(request):
        cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
        return render(request, "selecionar_cliente.html", {"cliente": cliente})
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def excluir_cliente(request, cliente_id):
    if get_status(request):
        cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
        if request.method == "POST":
            # Lógica para excluir o cliente
            return redirect("cliente/lista_clientes")
        else:
            return render(request, "excluir_cliente.html", {"cliente": cliente})
    else:
        return erro(request, "Você não está autorizado a fazer esta requisição.")


def home_cliente(request):

    return render(request, "cliente/default/home.html")
