from django.shortcuts import render, redirect
from ..def_global import criar_alerta_js, erro
from ..models.usuario import Usuario
from ..models.produto import Loja, Produto
from ..models.venda import Venda
from ..models.cliente import Cliente
from ..models.galao import Galao


def home_cliente(request):
    # Verifica se a chave 'primeiro_acesso' está presente na sessão do usuário
    if "primeiro_acesso" not in request.session:
        # Se for o primeiro acesso, define a chave 'primeiro_acesso' na sessão
        request.session["primeiro_acesso"] = True
        alerta_js = criar_alerta_js("Olá, seja Bem vindo")
    else:
        # Se não for o primeiro acesso, não exibe a mensagem de boas-vindas
        alerta_js = ""

    return render(request, "cliente/default/home.html", {"alerta_js": alerta_js})


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(
        request, "cliente/usuario/listar_usuario.html", {"usuarios": usuarios}
    )


def lista_lojas(request):
    lojas = Loja.objects.all()
    return render(request, "lista_lojas.html", {"lojas": lojas})


def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "lista_produtos.html", {"produtos": produtos})


def lista_vendas(request):
    vendas = Venda.objects.all()
    return render(request, "lista_vendas.html", {"vendas": vendas})


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "lista_clientes.html", {"clientes": clientes})


def lista_galoes(request):
    galoes = Galao.objects.all()
    return render(request, "lista_galoes.html", {"galoes": galoes})
