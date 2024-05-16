from django.urls import path
from app.view.sessao import views_sessao

app_name = "app"
from django.conf import settings
from django.conf.urls.static import static
from app.view.views_default import views_default
from app.utils import utils

url_default = [
    path("", views_default.home, name=""),
    path("home", views_default.home, name="home"),
    path("cadastro/", views_default.cadastro, name="cadastro"),
    path("login/", views_default.login, name="login"),
    path("sobre/", views_default.sobre, name="sobre"),
    path("Erro/", utils.erro, name="Erro"),
]

from app.view.assinante import views_assinante

url_assinante = [
    path("dashbord/", views_assinante.dashbord, name="dashbord"),
    path("desconect/", views_assinante.desconect, name="desconect"),
]

from app.view.views_empresa import views_empresa

url_empresa = [  # empresa
    path("empresas/", views_empresa.listar_empresas, name="listar_empresas"),
    path("empresas/criar/", views_empresa.criar_empresa, name="criar_empresa"),
    path("empresas/<int:pk>/", views_empresa.detalhes_empresa, name="detalhes_empresa"),
    path(
        "empresas/<int:pk>/editar/", views_empresa.editar_empresa, name="editar_empresa"
    ),
    path(
        "empresas/<int:pk>/excluir/",
        views_empresa.excluir_empresa,
        name="excluir_empresa",
    ),
]

from app.view.views_usuario import views_usuarios

url_usuario = [
    # URLs de usuários
    path("usuarios/", views_usuarios.listar_usuarios, name="listar_usuarios"),
    path("usuarios/criar/", views_usuarios.cadastrar_usuario, name="cadastrar_usuario"),
    path(
        "usuarios/<int:id_usuario>/",
        views_usuarios.detalhes_usuario,
        name="detalhes_usuario",
    ),
    path(
        "usuarios/<int:id_usuario>/editar/",
        views_usuarios.editar_usuario,
        name="editar_usuario",
    ),
    path(
        "usuarios/excluir/<int:id_usuario>",
        views_usuarios.excluir_usuario,
        name="excluir_usuario",
    ),
    path(
        "usuarios/bloquear/<int:id_usuario>",
        views_usuarios.bloquear_usuario,
        name="bloquear_usuario",
    ),
    path(
        "usuarios/configuracao/<int:id_usuario>",
        views_usuarios.configuracao_usuario,
        name="configuracao_usuario",
    ),
    path(
        "usuarios/ativar/<int:id_usuario>",
        views_usuarios.ativar_usuario,
        name="ativar_usuario",
    ),
]
from app.view.views_loja import views_loja

url_loja = [
    # lojas
    path("lojas/", views_loja.lista_lojas, name="lista_lojas"),
    path("lojas/criar", views_loja.criar_loja, name="criar_loja"),
    path("lojas/editar/<int:id_loja>/", views_loja.editar_loja, name="editar_loja"),
    path(
        "lojas/selecionar/<int:id_loja>/",
        views_loja.selecionar_loja,
        name="selecionar_loja",
    ),
    path("lojas/excluir/<int:id_loja>/", views_loja.excluir_loja, name="excluir_loja"),
]


from app.view.views_produto import views_produto

url_produto = [  # produtos
    path("produtos/", views_produto.lista_produtos, name="lista_produtos"),
    path(
        "produtos/editar/<uuid:id_produto>/",
        views_produto.form_produto,
        name="editar_produto",
    ),
    path(
        "produtos/acrescentar/",
        views_produto.acrescentar_produto,
        name="acrescentar_produto",
    ),
    path("produtos/criar/", views_produto.form_produto, name="criar_produto"),
    path(
        "produtos/selecionar/<uuid:id_produto>/",
        views_produto.selecionar_produto,
        name="selecionar_produto",
    ),
    path(
        "produtos/excluir/<uuid:id_produto>/",
        views_produto.excluir_produto,
        name="excluir_produto",
    ),
]

from app.view.views_venda import views_venda

url_venda = [  # vendas
    path("vendas/", views_venda.lista_vendas, name="lista_vendas"),
    path("vendas/criar/", views_venda.criar_venda, name="criar_venda"),
    path(
        "vendas/editar/<uuid:id_venda>/", views_venda.editar_venda, name="editar_venda"
    ),
    path(
        "vendas/selecionar/<uuid:id_venda>/",
        views_venda.selecionar_venda,
        name="selecionar_venda",
    ),
    path(
        "vendas/excluir/<uuid:id_venda>/",
        views_venda.excluir_venda,
        name="excluir_venda",
    ),
    path(
        "vendas/criar/insert_venda_ajax/",
        views_venda.insert_venda_ajax,
        name="insert_venda_ajax",
    ),
    path(
        "api/vendas/dados",
        views_venda.obter_dados,
        name="api_obter_dados_vendas",
    ),
    path(
        "api/cliente/by/venda/<uuid:id_venda>",
        views_venda.selecionar_cliente_by_venda,
        name="selecionar_cliente_by_vendas",
    ),
    path(
        "api/produtos/by/venda/<uuid:id_venda>",
        views_venda.selecionar_produto_by_venda,
        name="selecionar_produto_by_vendas",
    ),
    path(
        "api/retornaveis/by/venda/<uuid:id_venda>",
        views_venda.selecionar_retornaveis_by_venda,
        name="selecionar_produto_by_vendas",
    ),
]

from app.view.views_cliente import views_cliente

url_cliente = [  # clientes
    path("clientes/", views_cliente.lista_clientes, name="lista_clientes"),
    path("clientes/criar/", views_cliente.criar_cliente, name="criar_cliente"),
    path(
        "clientes/editar/<uuid:id_cliente>/",
        views_cliente.editar_cliente,
        name="editar_cliente",
    ),
    path(
        "clientes/selecionar/<uuid:id_cliente>/",
        views_cliente.selecionar_cliente,
        name="selecionar_cliente",
    ),
    path(
        "clientes/excluir/<uuid:id_cliente>/",
        views_cliente.excluir_cliente,
        name="excluir_cliente",
    ),
    path(
        "api_get_vendas_by_cliente/<uuid:id_cliente>",
        views_cliente.api_get_vendas_by_cliente,
        name="vendas_clientes",
    ),
     path(
        "api/cliente/create/",
        views_cliente.api_create_update_cliente,
        name="api_create_cliente",
    ),
    path(
        "api/cliente/<uuid:cliente_id>/",
        views_cliente.api_get_cliente,
        name="api_get_cliente",
    ),
    path(
        "api/cliente/<uuid:cliente_id>/update/",
        views_cliente.api_update_cliente,
        name="api_update_cliente",
    ),
    path(
        "api/cliente/<uuid:cliente_id>/delete/",
        views_cliente.api_delete_cliente,
        name="api_delete_cliente",
    ),
    path(
        "api/cliente/by_empresa/",
        views_cliente.api_get_clientes_by_empresa,
        name="api_get_clientes_by_empresa",
    ),
]

from app.view.views_galao import views_galao

url_galao = [  ##galoes
    path("galoes/", views_galao.lista_galao, name="lista_galoes"),
    path("galoes/criar", views_galao.editar_galao, name="criar_galao"),
    path(
        "galoes/editar/<int:galao_id>/", views_galao.editar_galao, name="editar_galao"
    ),
    path(
        "galoes/selecionar/<int:galao_id>/",
        views_galao.selecionar_galao,
        name="selecionar_galao",
    ),
    path(
        "galoes/excluir/<int:galao_id>/",
        views_galao.excluir_galao,
        name="excluir_galao",
    ),
]

from app.view.views_endereco import views_endereco

url_endereco = [
    path("endereco/", views_endereco.lista_enderecos, name="lista_enderecos"),
    path("endereco/criar/", views_endereco.criar_endereco, name="criar_endereco"),
    path(
        "endereco/<int:pk>/",
        views_endereco.selecionar_endereco,
        name="selecionar_endereco",
    ),
    path(
        "endereco/<int:pk>/editar/",
        views_endereco.editar_endereco,
        name="editar_endereco",
    ),
    path(
        "endereco/<int:pk>/excluir/",
        views_endereco.delete_endereco,
        name="delete_endereco",
    ),
]

from app.view.view_api import views_api

url_funcJs = [  # funçoes js
    path("enviar-codigo/<str:email>/", utils.enviar_codigo, name="enviar_codigo"),
    path(
        "confirmar-codigo/<str:codigo>/",
        utils.confirmar_codigo,
        name="confirmar_codigo",
    ),
    path(
        "atualizar-senha/<str:nova_senha>/",
        utils.atualizar_senha,
        name="atualizar_senha",
    ),
    path("api/status_on/", views_sessao.status_on, name="status_on"),
    path("api/status_off/", views_sessao.status_off, name="status_off"),
    path("buscar_lojas/", views_api.buscar_lojas, name="buscar_lojas"),
    path("endereco/create/", views_api.create_endereco, name="create_endereco"),
    path(
        "endereco/read/<str:endereco_id>/",
        views_api.read_endereco,
        name="read_endereco",
    ),
    path(
        "endereco/update/<str:endereco_id>/",
        views_api.update_endereco,
        name="update_endereco",
    ),
    path(
        "endereco/delete/<str:endereco_id>/",
        views_api.delete_endereco,
        name="delete_endereco",
    ),
    # Adicione outras URLs conforme necessário
]
from app.view.views_configuracao import views_configuracao

url_configuracao = []

from app.view.views_motoboy import views_motoboy

url_motoboy = [
    path(
        "listar_motoboys_por_empresa/",
        views_motoboy.listar_motoboys_por_empresa,
        name="listar_motoboys_por_empresa",
    ),
    path("create_motoboy/", views_motoboy.create_motoboy, name="create_motoboy"),
    path(
        "update_motoboy/<str:id_motoboy>/",
        views_motoboy.update_motoboy,
        name="update_motoboy",
    ),
    path(
        "delete_motoboy/<str:id_motoboy>/",
        views_motoboy.delete_motoboy,
        name="delete_motoboy",
    ),
    path(
        "get_motoboy_by_venda/<uuid:id_venda>/",
        views_motoboy.get_motoboy_by_venda,
        name="get_motoboy_by_venda",
    ),
]


from app.view.views_cliente import views_cliente
 

urlpatterns = (
    url_default
    + url_funcJs
    + url_assinante
    + url_empresa
    + url_usuario
    + url_venda
    + url_produto
    + url_loja
    + url_cliente
    + url_endereco
    + url_galao
    + url_motoboy
)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
