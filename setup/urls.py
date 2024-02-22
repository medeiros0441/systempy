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

from app.view.views_loja import (
    lista_lojas,
    editar_loja,
    selecionar_loja,
    excluir_loja,
)
from app.view.views_produto import (
    lista_produtos,
    editar_produto,
    selecionar_produto,
    excluir_produto,
)
from app.view.views_venda import (
    lista_vendas,
    editar_venda,
    selecionar_venda,
    excluir_venda,
)
from app.view.views_cliente import (
    lista_clientes,
    criar_cliente,
    editar_cliente,
    selecionar_cliente,
    excluir_cliente,
)
from app.view.views_galao import (
    lista_galoes,
    editar_galao,
    selecionar_galao,
    excluir_galao,
)

from app.view.sessao import status_off, status_on
from app.def_global import (
    enviar_codigo,
    atualizar_senha,
    confirmar_codigo,
)
from django.conf import settings
from django.conf.urls.static import static
from app.view.assinante import home as a_home

app_name = "app"

urlpatterns = [
    path("", home, name=""),
    path("home", home, name="home"),
    path("cadastro/", cadastro, name="cadastro"),
    path("login/", login, name="login"),
    path("sobre/", sobre, name="sobre"),
    path("Erro/", erro, name="Erro"),
    path("assinante/", a_home, name="assinante"),
    # empresa
    path("empresas/", listar_empresas, name="listar_empresas"),
    path("empresas/criar/", criar_empresa, name="criar_empresa"),
    path("empresas/<int:pk>/", detalhes_empresa, name="detalhes_empresa"),
    path("empresas/<int:pk>/editar/", editar_empresa, name="editar_empresa"),
    path("empresas/<int:pk>/excluir/", excluir_empresa, name="excluir_empresa"),
    # usuarios
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
    # lojas
    path("lojas/", lista_lojas, name="lista_lojas"),
    path("lojas/editar/<int:loja_id>/", editar_loja, name="editar_loja"),
    path("lojas/selecionar/<int:loja_id>/", selecionar_loja, name="selecionar_loja"),
    path("lojas/excluir/<int:loja_id>/", excluir_loja, name="excluir_loja"),
    # produtos
    path("produtos/", lista_produtos, name="lista_produtos"),
    path("produtos/editar/<int:produto_id>/", editar_produto, name="editar_produto"),
    path(
        "produtos/selecionar/<int:produto_id>/",
        selecionar_produto,
        name="selecionar_produto",
    ),
    path("produtos/excluir/<int:produto_id>/", excluir_produto, name="excluir_produto"),
    # vendas
    path("vendas/", lista_vendas, name="lista_vendas"),
    path("vendas/editar/<int:venda_id>/", editar_venda, name="editar_venda"),
    path(
        "vendas/selecionar/<int:venda_id>/", selecionar_venda, name="selecionar_venda"
    ),
    path("vendas/excluir/<int:venda_id>/", excluir_venda, name="excluir_venda"),
    # clientes
    path("clientes/", lista_clientes, name="lista_clientes"),
    path("clientes/criar/", criar_cliente, name="criar_cliente"),
    path("clientes/editar/<int:cliente_id>/", editar_cliente, name="editar_cliente"),
    path(
        "clientes/selecionar/<int:cliente_id>/",
        selecionar_cliente,
        name="selecionar_cliente",
    ),
    path("clientes/excluir/<int:cliente_id>/", excluir_cliente, name="excluir_cliente"),
    ##galoes
    path("galoes/", lista_galoes, name="lista_galoes"),
    path("galoes/editar/<int:galao_id>/", editar_galao, name="editar_galo"),
    path("galoes/selecionar/<int:galao_id>/", selecionar_galao, name="selecionar_galo"),
    path("galoes/excluir/<int:galao_id>/", excluir_galao, name="excluir_galo"),
    # funçoes js
    path("enviar-codigo/<str:email>/", enviar_codigo, name="enviar_codigo"),
    path("confirmar-codigo/<str:codigo>/", confirmar_codigo, name="confirmar_codigo"),
    path("atualizar-senha/<str:nova_senha>/", atualizar_senha, name="atualizar_senha"),
    path("api/status_on/", status_on, name="status_on"),
    path("api/status_off/", status_off, name="status_off"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
