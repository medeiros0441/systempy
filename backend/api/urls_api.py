from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from api.utils import Utils
import api.views as views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from views import ViewsPublic
from api.views import ViewCliente

from .TokenManager import TokenManager
router = DefaultRouter()
router.register(r"public", ViewsPublic, basename="public")
router.register(r'clientes', ViewCliente, basename='cliente')


url_public = [
    path("", include(router.urls)),
    path("csrfToken/", TokenManager.csrf_token_view, name="csrfToken"),
    path("status_on", views.views_sessao.status_on, name="status_on"),
    path("status_off", views.views_sessao.status_off, name="status_off"),
]

url_erros = [
    path("erro", views.views_erro.erro, name="erro"),
    path(
        "erro/404",
        views.views_erro.erro,
        {"error_message": "Página não encontrada"},
        name="erro_404",
    ),
    path(
        "erro/500",
        views.views_erro.erro,
        {"error_message": "Erro interno do servidor"},
        name="erro_500",
    ),
    path(
        "erro/403",
        views.views_erro.erro,
        {"error_message": "Acesso negado"},
        name="erro_403",
    ),
    path(
        "erro/400",
        views.views_erro.erro,
        {"error_message": "Requisição inválida"},
        name="erro_400",
    ),
]


url_empresa = [  # empresa
    path("list_empresas", views.views_empresa.list_empresas, name="list_empresas"),
    path(
        "create_empresa",
        views.views_empresa.create_empresa,
        name="create_empresa",
    ),
    path("get_empresa", views.views_empresa.get_empresa, name="get_empresa"),
    path(
        "get_empresa/<uuid:id>",
        views.views_empresa.get_empresa,
        name="get_empresa",
    ),
    path(
        "update_empresa/<uuid:id>",
        views.views_empresa.update_empresa,
        name="update_empresa",
    ),
    path(
        "delete_empresa/<uuid:id>",
        views.views_empresa.delete_empresa,
        name="delete_empresa",
    ),
]

url_pdv = [
    path("pdv", views.views_pdv.pdv, name="pdv"),
    # URLs para views_pdv
    path("pdv/lista", views.views_pdv.list_pdv, name="list_pdv"),
    path("pdv/<uuid:id_loja>", views.views_pdv.list_pdv, name="list_pdv"),
    path("pdv/create", views.views_pdv.create_pdv, name="create_pdv"),
    path("pdv/update", views.views_pdv.update_pdv, name="update_pdv"),
    # URLs para views_registro_diario_pdv
    path(
        "registro_diario_pdv/<uuid:id_pdv>",
        views.views_registro_diario_pdv.list_registro_diario_pdv,
        name="list_registro_diario_pdv",
    ),
    path(
        "registro_diario_pdv/create/<uuid:id>",
        views.views_registro_diario_pdv.create_registro_diario_pdv,
        name="update_registro_diario_pdv",
    ),
    path(
        "registro_diario_pdv/update",
        views.views_registro_diario_pdv.update_registro_diario_pdv,
        name="update_registro_diario_pdv",
    ),
    # URLs para views_associado_pdv
    path(
        "associado_pdv",
        views.views_associado_pdv.list_associado_pdv,
        name="list_associado_pdv",
    ),
    path(
        "associado_pdv/create",
        views.views_associado_pdv.create_associado_pdv,
        name="create_associado_pdv",
    ),
    path(
        "associado_pdv/update",
        views.views_associado_pdv.update_associado_pdv,
        name="update_associado_pdv",
    ),
]

url_usuario = [
    path(
        "usuarios/criar",
        views.views_usuarios.cadastrar_usuario,
        name="cadastrar_usuario",
    ),
    path(
        "usuarios/excluir/<uuid:id_usuario>",
        views.views_usuarios.excluir_usuario,
        name="excluir_usuario",
    ),
    path(
        "usuarios/bloquear/<uuid:id_usuario>",
        views.views_usuarios.bloquear_usuario,
        name="bloquear_usuario",
    ),
    path(
        "usuarios/configuracao/<uuid:id_usuario>",
        views.views_usuarios.configuracao_usuario,
        name="configuracao_usuario",
    ),
    path(
        "usuarios/ativar/<uuid:id_usuario>",
        views.views_usuarios.ativar_usuario,
        name="ativar_usuario",
    ),
]

ur_personalizacao = [
    path(
        "personalizacao/create",
        views.views_personalizacao.create_personalizacao,
        name="create_personalizacao",
    ),
    path(
        "personalizacao/<uuid:id>",
        views.views_personalizacao.get_personalizacao,
        name="get_personalizacao",
    ),
    path(
        "personalizacao/update/<uuid:id>",
        views.views_personalizacao.update_personalizacao,
        name="update_personalizacao",
    ),
    path(
        "personalizacao/delete/<uuid:id>",
        views.views_personalizacao.delete_personalizacao,
        name="delete_personalizacao",
    ),
    path(
        "personalizacao/list",
        views.views_personalizacao.list_personalizacao,
        name="list_personalizacao",
    ),
    path(
        "get_personalizacao_for_venda",
        views.views_personalizacao.get_personalizacao_for_venda,
        name="get_personalizacao_for_venda",
    ),
]
url_loja = [
    # lojas
    path("lojas", views.views_loja.lista_lojas, name="lista_lojas"),
    path("lojas/criar", views.views_loja.criar_loja, name="criar_loja"),
    path("lojas/editar/<int:id_loja>", views.views_loja.editar_loja, name="editar_loja"),
    path(
        "lojas/selecionar/<int:id_loja>",
        views.views_loja.selecionar_loja,
        name="selecionar_loja",
    ),
    path(
        "lojas/excluir/<int:id_loja>",
        views.views_loja.excluir_loja,
        name="excluir_loja",
    ),
]


url_produto = [
    path(
        "produtos/editar/<uuid:id_produto>",
        views.views_produto.form_produto,
        name="editar_produto",
    ),
    path(
        "produtos/acrescentar",
        views.views_produto.acrescentar_produto,
        name="acrescentar_produto",
    ),
    path("produtos/criar", views.views_produto.form_produto, name="criar_produto"),
    path(
        "produtos/selecionar/<uuid:id_produto>",
        views.views_produto.selecionar_produto,
        name="selecionar_produto",
    ),
    path(
        "produtos/excluir/<uuid:id_produto>",
        views.views_produto.excluir_produto,
        name="excluir_produto",
    ),
]


router = DefaultRouter()
router.register(r"vendas", views.views_venda, basename="venda")


url_cliente = [  # clientes
    path("clientes/criar", views.ClienteViewSet.create_cliente, name="criar_cliente"),
    path(
        "get_vendas_by_cliente/<uuid:id_cliente>",
        views.ClienteViewSet.get_vendas_by_cliente,
        name="vendas_clientes",
    ),
    path(
        "cliente/create",
        views.ClienteViewSet.create_cliente,
        name="create_cliente",
    ),
    path(
        "cliente/<uuid:cliente_id>",
        views.ClienteViewSet.get_cliente,
        name="get_cliente",
    ),
    path(
        "cliente/update",
        views.ClienteViewSet.update_cliente,
        name="update_cliente",
    ),
    path(
        "cliente/<uuid:cliente_id>/delete",
        views.ClienteViewSet.delete_cliente,
        name="delete_cliente",
    ),
    path(
        "cliente/by_empresa",
        views.ClienteViewSet.get_clientes_by_empresa,
        name="get_clientes_by_empresa",
    ),
]

url_galao = [  ##galoes
    path("galoes", views.views_galao.lista_galao, name="lista_galoes"),
    path("galoes/criar", views.views_galao.editar_galao, name="criar_galao"),
    path(
        "galoes/editar/<int:galao_id>",
        views.views_galao.editar_galao,
        name="editar_galao",
    ),
    path(
        "galoes/selecionar/<int:galao_id>",
        views.views_galao.selecionar_galao,
        name="selecionar_galao",
    ),
    path(
        "galoes/excluir/<int:galao_id>",
        views.views_galao.excluir_galao,
        name="excluir_galao",
    ),
]


url_motoboy = [
    path(
        "listar_motoboys_por_empresa",
        views.views_motoboy.listar_motoboys_por_empresa,
        name="listar_motoboys_por_empresa",
    ),
    path("create_motoboy", views.views_motoboy.create_motoboy, name="create_motoboy"),
    path(
        "update_motoboy/<str:id_motoboy>",
        views.views_motoboy.update_motoboy,
        name="update_motoboy",
    ),
    path(
        "delete_motoboy/<str:id_motoboy>",
        views.views_motoboy.delete_motoboy,
        name="delete_motoboy",
    ),
    path(
        "get_motoboy_by_venda/<uuid:id_venda>",
        views.views_motoboy.get_motoboy_by_venda,
        name="get_motoboy_by_venda",
    ),
]


urlpatterns = (
    url_public
    + url_empresa
    + url_usuario
    + url_produto
    + url_loja
    + url_cliente
    + url_galao
    + url_motoboy
    + url_erros
    + url_pdv
    + ur_personalizacao
)
