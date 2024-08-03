from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from api.utils import Utils
import api.view as view
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .view import views_public

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .TokenManager import TokenManager
router = DefaultRouter()
router.register(r"public", views_public, basename="public")

url_public = [
    path("", include(router.urls)),
    path("csrfToken/", TokenManager.csrf_token_view, name="csrfToken"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("status_on", view.views_sessao.status_on, name="status_on"),
    path("status_off", view.views_sessao.status_off, name="status_off"),
]

url_erros = [
    path("erro", view.views_erro.erro, name="erro"),
    path(
        "erro/404",
        view.views_erro.erro,
        {"error_message": "Página não encontrada"},
        name="erro_404",
    ),
    path(
        "erro/500",
        view.views_erro.erro,
        {"error_message": "Erro interno do servidor"},
        name="erro_500",
    ),
    path(
        "erro/403",
        view.views_erro.erro,
        {"error_message": "Acesso negado"},
        name="erro_403",
    ),
    path(
        "erro/400",
        view.views_erro.erro,
        {"error_message": "Requisição inválida"},
        name="erro_400",
    ),
]


url_empresa = [  # empresa
    path("list_empresas", view.views_empresa.list_empresas, name="list_empresas"),
    path(
        "create_empresa",
        view.views_empresa.create_empresa,
        name="create_empresa",
    ),
    path("get_empresa", view.views_empresa.get_empresa, name="get_empresa"),
    path(
        "get_empresa/<uuid:id>",
        view.views_empresa.get_empresa,
        name="get_empresa",
    ),
    path(
        "update_empresa/<uuid:id>",
        view.views_empresa.update_empresa,
        name="update_empresa",
    ),
    path(
        "delete_empresa/<uuid:id>",
        view.views_empresa.delete_empresa,
        name="delete_empresa",
    ),
]

url_pdv = [
    path("pdv", view.views_pdv.pdv, name="pdv"),
    # URLs para views_pdv
    path("pdv/lista", view.views_pdv.list_pdv, name="list_pdv"),
    path("pdv/<uuid:id_loja>", view.views_pdv.list_pdv, name="list_pdv"),
    path("pdv/create", view.views_pdv.create_pdv, name="create_pdv"),
    path("pdv/update", view.views_pdv.update_pdv, name="update_pdv"),
    # URLs para views_registro_diario_pdv
    path(
        "registro_diario_pdv/<uuid:id_pdv>",
        view.views_registro_diario_pdv.list_registro_diario_pdv,
        name="list_registro_diario_pdv",
    ),
    path(
        "registro_diario_pdv/create/<uuid:id>",
        view.views_registro_diario_pdv.create_registro_diario_pdv,
        name="update_registro_diario_pdv",
    ),
    path(
        "registro_diario_pdv/update",
        view.views_registro_diario_pdv.update_registro_diario_pdv,
        name="update_registro_diario_pdv",
    ),
    # URLs para views_associado_pdv
    path(
        "associado_pdv",
        view.views_associado_pdv.list_associado_pdv,
        name="list_associado_pdv",
    ),
    path(
        "associado_pdv/create",
        view.views_associado_pdv.create_associado_pdv,
        name="create_associado_pdv",
    ),
    path(
        "associado_pdv/update",
        view.views_associado_pdv.update_associado_pdv,
        name="update_associado_pdv",
    ),
]

url_usuario = [
    path(
        "usuarios/criar",
        view.views_usuarios.cadastrar_usuario,
        name="cadastrar_usuario",
    ),
    path(
        "usuarios/excluir/<uuid:id_usuario>",
        view.views_usuarios.excluir_usuario,
        name="excluir_usuario",
    ),
    path(
        "usuarios/bloquear/<uuid:id_usuario>",
        view.views_usuarios.bloquear_usuario,
        name="bloquear_usuario",
    ),
    path(
        "usuarios/configuracao/<uuid:id_usuario>",
        view.views_usuarios.configuracao_usuario,
        name="configuracao_usuario",
    ),
    path(
        "usuarios/ativar/<uuid:id_usuario>",
        view.views_usuarios.ativar_usuario,
        name="ativar_usuario",
    ),
]

ur_personalizacao = [
    path(
        "personalizacao/create",
        view.views_personalizacao.create_personalizacao,
        name="create_personalizacao",
    ),
    path(
        "personalizacao/<uuid:id>",
        view.views_personalizacao.get_personalizacao,
        name="get_personalizacao",
    ),
    path(
        "personalizacao/update/<uuid:id>",
        view.views_personalizacao.update_personalizacao,
        name="update_personalizacao",
    ),
    path(
        "personalizacao/delete/<uuid:id>",
        view.views_personalizacao.delete_personalizacao,
        name="delete_personalizacao",
    ),
    path(
        "personalizacao/list",
        view.views_personalizacao.list_personalizacao,
        name="list_personalizacao",
    ),
    path(
        "get_personalizacao_for_venda",
        view.views_personalizacao.get_personalizacao_for_venda,
        name="get_personalizacao_for_venda",
    ),
]
url_loja = [
    # lojas
    path("lojas", view.views_loja.lista_lojas, name="lista_lojas"),
    path("lojas/criar", view.views_loja.criar_loja, name="criar_loja"),
    path("lojas/editar/<int:id_loja>", view.views_loja.editar_loja, name="editar_loja"),
    path(
        "lojas/selecionar/<int:id_loja>",
        view.views_loja.selecionar_loja,
        name="selecionar_loja",
    ),
    path(
        "lojas/excluir/<int:id_loja>",
        view.views_loja.excluir_loja,
        name="excluir_loja",
    ),
]


url_produto = [
    path(
        "produtos/editar/<uuid:id_produto>",
        view.views_produto.form_produto,
        name="editar_produto",
    ),
    path(
        "produtos/acrescentar",
        view.views_produto.acrescentar_produto,
        name="acrescentar_produto",
    ),
    path("produtos/criar", view.views_produto.form_produto, name="criar_produto"),
    path(
        "produtos/selecionar/<uuid:id_produto>",
        view.views_produto.selecionar_produto,
        name="selecionar_produto",
    ),
    path(
        "produtos/excluir/<uuid:id_produto>",
        view.views_produto.excluir_produto,
        name="excluir_produto",
    ),
]


router = DefaultRouter()
router.register(r"vendas", view.views_venda, basename="venda")


url_cliente = [  # clientes
    path("clientes/criar", view.views_cliente.create_cliente, name="criar_cliente"),
    path(
        "get_vendas_by_cliente/<uuid:id_cliente>",
        view.views_cliente.get_vendas_by_cliente,
        name="vendas_clientes",
    ),
    path(
        "cliente/create",
        view.views_cliente.create_cliente,
        name="create_cliente",
    ),
    path(
        "cliente/<uuid:cliente_id>",
        view.views_cliente.get_cliente,
        name="get_cliente",
    ),
    path(
        "cliente/update",
        view.views_cliente.update_cliente,
        name="update_cliente",
    ),
    path(
        "cliente/<uuid:cliente_id>/delete",
        view.views_cliente.delete_cliente,
        name="delete_cliente",
    ),
    path(
        "cliente/by_empresa",
        view.views_cliente.get_clientes_by_empresa,
        name="get_clientes_by_empresa",
    ),
]

url_galao = [  ##galoes
    path("galoes", view.views_galao.lista_galao, name="lista_galoes"),
    path("galoes/criar", view.views_galao.editar_galao, name="criar_galao"),
    path(
        "galoes/editar/<int:galao_id>",
        view.views_galao.editar_galao,
        name="editar_galao",
    ),
    path(
        "galoes/selecionar/<int:galao_id>",
        view.views_galao.selecionar_galao,
        name="selecionar_galao",
    ),
    path(
        "galoes/excluir/<int:galao_id>",
        view.views_galao.excluir_galao,
        name="excluir_galao",
    ),
]


url_motoboy = [
    path(
        "listar_motoboys_por_empresa",
        view.views_motoboy.listar_motoboys_por_empresa,
        name="listar_motoboys_por_empresa",
    ),
    path("create_motoboy", view.views_motoboy.create_motoboy, name="create_motoboy"),
    path(
        "update_motoboy/<str:id_motoboy>",
        view.views_motoboy.update_motoboy,
        name="update_motoboy",
    ),
    path(
        "delete_motoboy/<str:id_motoboy>",
        view.views_motoboy.delete_motoboy,
        name="delete_motoboy",
    ),
    path(
        "get_motoboy_by_venda/<uuid:id_venda>",
        view.views_motoboy.get_motoboy_by_venda,
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
