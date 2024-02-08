from django.urls import path
from app.view.views import home, cadastro, login, sobre, erro
from app.view.views_empresa import (
    listar_empresas,
    criar_empresa,
    detalhes_empresa,
    editar_empresa,
    excluir_empresa,
)
from app.view.views_usuario import (
    listar_usuarios,
    cadastrar_usuario,
    detalhes_usuario,
    excluir_usuario,
    ativar_usuario,
    bloquear_usuario,
)
from app.view.views_cliente import (
    home_cliente,
    lista_lojas,
    lista_produtos,
    lista_vendas,
    lista_clientes,
    lista_galoes,
)
from app.def_global import enviar_codigo, atualizar_senha, confirmar_codigo

app_name = "app"

urlpatterns = [
    path("", home, name=""),
    path("home", home, name="home"),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("sobre/", sobre, name="sobre"),
    path("Erro/", erro, name="Erro"),
    # path for client
    path("cliente/default/", home_cliente, name="cliente"),
    path("cliente/default/", home_cliente, name="home_cliente"),
    path("lojas/", lista_lojas, name="lista_lojas"),
    path("produtos/", lista_produtos, name="lista_produtos"),
    path("vendas/", lista_vendas, name="lista_vendas"),
    path("clientes/", lista_clientes, name="lista_clientes"),
    path("galoes/", lista_galoes, name="lista_galoes"),
    # Outras URLs...
    # URLs relacionadas a empresas
    path("empresas/", listar_empresas, name="listar_empresas"),
    path("empresas/criar/", criar_empresa, name="criar_empresa"),
    path("empresas/<int:pk>/", detalhes_empresa, name="detalhes_empresa"),
    path("empresas/<int:pk>/editar/", editar_empresa, name="editar_empresa"),
    path("empresas/<int:pk>/excluir/", excluir_empresa, name="excluir_empresa"),
    # URLs relacionadas a usuários
    path("usuarios/", listar_usuarios, name="listar_usuarios"),
    path(
        "usuarios/bloquear/<int:id_usuario>/'",
        bloquear_usuario,
        name="bloquear_usuario",
    ),
    path("usuarios/ativar/<int:id_usuario>/'", ativar_usuario, name="ativar_usuario"),
    path("usuarios/criar/", cadastrar_usuario, name="cadastrar_usuario"),
    path("usuarios/<int:id_usuario>/", detalhes_usuario, name="detalhes_usuario"),
    path(
        "usuarios/<int:id_usuario>/editar_usuario/",
        cadastrar_usuario,
        name="editar_usuario",
    ),
    path("usuarios/<int:id_usuario>/excluir/", excluir_usuario, name="excluir_usuario"),
    # funçoes
    path("enviar-codigo/<str:email>/", enviar_codigo, name="enviar_codigo"),
    path("confirmar-codigo/<str:codigo>/", confirmar_codigo, name="confirmar_codigo"),
    path("atualizar-senha/<str:nova_senha>/", atualizar_senha, name="atualizar_senha"),
]
