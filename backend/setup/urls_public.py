from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from app.utils import Utils
import app.view as view
from django.views.generic import TemplateView

aurlpatterns2314 = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("home", view.views_default.home, name="home"),
    path("cadastro", view.views_default.cadastro, name="cadastro"),
    path("login", view.views_default.login, name="login"),
    path("sobre", view.views_default.sobre, name="sobre"),
]


urlpatterns = [
    path(
        "", TemplateView.as_view(template_name="index.html")
    ),  # Servir o React index.html
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
    # Adicione outras rotas de erro conforme necessário
]

 
url_assinante = [
    path("dashboard", view.views_assinante.dashboard, name="dashboard"),
    path("desconect", view.views_assinante.desconect, name="desconect"),
    path("configuracao", view.views_assinante.configuracao, name="configuracao"),
]


url_empresa = [  # empresa
    path("empresas", view.views_empresa.listar_empresas, name="listar_empresas"),
    path("empresas/criar", view.views_empresa.criar_empresa, name="criar_empresa"),
    path(
        "empresas/<uuid:pk>",
        view.views_empresa.detalhes_empresa,
        name="detalhes_empresa",
    ),
    path(
        "empresas/<uuid:pk>/editar",
        view.views_empresa.editar_empresa,
        name="editar_empresa",
    ),
    path(
        "empresas/<uuid:pk>/excluir",
        view.views_empresa.excluir_empresa,
        name="excluir_empresa",
    ),
    path(
        "api_list_empresas", view.views_empresa.list_empresas, name="api_list_empresas"
    ),
    path(
        "api_create_empresa",
        view.views_empresa.create_empresa,
        name="api_create_empresa",
    ),
    path("api_get_empresa", view.views_empresa.get_empresa, name="api_get_empresa"),
    path(
        "api_get_empresa/<uuid:id>",
        view.views_empresa.get_empresa,
        name="api_get_empresa",
    ),
    path(
        "api_update_empresa/<uuid:id>",
        view.views_empresa.update_empresa,
        name="api_update_empresa",
    ),
    path(
        "api_delete_empresa/<uuid:id>",
        view.views_empresa.delete_empresa,
        name="api_delete_empresa",
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
    # URLs de usuários
    path("usuarios", view.views_usuarios.listar_usuarios, name="listar_usuarios"),
    path(
        "api_usuarios",
        view.views_usuarios.api_listar_usuarios,
        name="api_listar_usuarios",
    ),
    path(
        "usuarios/criar",
        view.views_usuarios.cadastrar_usuario,
        name="cadastrar_usuario",
    ),
    path(
        "usuarios/<uuid:id_usuario>",
        view.views_usuarios.detalhes_usuario,
        name="detalhes_usuario",
    ),
    path(
        "usuarios/<uuid:id_usuario>/editar",
        view.views_usuarios.editar_usuario,
        name="editar_usuario",
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
    path("api_lojas", view.views_loja.api_lista_lojas, name="api_lista_lojas"),
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


url_produto = [  # produtos
    path("produtos", view.views_produto.lista_produtos, name="lista_produtos"),
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


url_venda = [  # vendas
    path("vendas", view.views_venda.lista_vendas, name="lista_vendas"),
    path("vendas/criar", view.views_venda.criar_venda, name="criar_venda"),
    path(
        "vendas/editar/<uuid:id_venda>",
        view.views_venda.editar_venda,
        name="editar_venda",
    ),
    path(
        "vendas/selecionar/<uuid:id_venda>",
        view.views_venda.selecionar_venda,
        name="selecionar_venda",
    ),
    path(
        "vendas/excluir/<uuid:id_venda>",
        view.views_venda.excluir_venda,
        name="excluir_venda",
    ),
    path(
        "vendas/criar/processar_venda",
        view.views_venda.processar_venda,
        name="processar_venda",
    ),
    path(
        "api/vendas/dados",
        view.views_venda.obter_dados,
        name="api_obter_dados_vendas",
    ),
    path(
        "api/cliente/by/venda/<uuid:id_venda>",
        view.views_venda.selecionar_cliente_by_venda,
        name="selecionar_cliente_by_vendas",
    ),
    path(
        "api/produtos/by/venda/<uuid:id_venda>",
        view.views_venda.selecionar_produto_by_venda,
        name="selecionar_produto_by_vendas",
    ),
    path(
        "api/retornaveis/by/venda/<uuid:id_venda>",
        view.views_venda.selecionar_retornaveis_by_venda,
        name="selecionar_produto_by_vendas",
    ),
]


url_cliente = [  # clientes
    path("clientes", view.views_cliente.lista_clientes, name="lista_clientes"),
    path("clientes/criar", view.views_cliente.criar_cliente, name="criar_cliente"),
    path(
        "clientes/editar/<uuid:id_cliente>",
        view.views_cliente.editar_cliente,
        name="editar_cliente",
    ),
    path(
        "clientes/selecionar/<uuid:id_cliente>",
        view.views_cliente.selecionar_cliente,
        name="selecionar_cliente",
    ),
    path(
        "clientes/excluir/<uuid:id_cliente>",
        view.views_cliente.excluir_cliente,
        name="excluir_cliente",
    ),
    path(
        "api_get_vendas_by_cliente/<uuid:id_cliente>",
        view.views_cliente.api_get_vendas_by_cliente,
        name="vendas_clientes",
    ),
    path(
        "api/cliente/create",
        view.views_cliente.api_create_cliente,
        name="api_create_cliente",
    ),
    path(
        "api/cliente/<uuid:cliente_id>",
        view.views_cliente.api_get_cliente,
        name="api_get_cliente",
    ),
    path(
        "api/cliente/update",
        view.views_cliente.api_update_cliente,
        name="api_update_cliente",
    ),
    path(
        "api/cliente/<uuid:cliente_id>/delete",
        view.views_cliente.api_delete_cliente,
        name="api_delete_cliente",
    ),
    path(
        "api/cliente/by_empresa",
        view.views_cliente.api_get_clientes_by_empresa,
        name="api_get_clientes_by_empresa",
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


url_endereco = [
    path("endereco", view.views_endereco.lista_enderecos, name="lista_enderecos"),
    path("endereco/criar", view.views_endereco.criar_endereco, name="criar_endereco"),
    path(
        "endereco/<int:pk>",
        view.views_endereco.selecionar_endereco,
        name="selecionar_endereco",
    ),
    path(
        "endereco/<int:pk>/editar",
        view.views_endereco.editar_endereco,
        name="editar_endereco",
    ),
    path(
        "endereco/<int:pk>/excluir",
        view.views_endereco.delete_endereco,
        name="delete_endereco",
    ),
    path(
        "endereco/read/<str:endereco_id>",
        view.views_api.read_endereco,
        name="read_endereco",
    ),
    path(
        "endereco/update/<str:endereco_id>",
        view.views_api.update_endereco,
        name="update_endereco",
    ),
    path(
        "endereco/delete/<str:endereco_id>",
        view.views_api.delete_endereco,
        name="delete_endereco",
    ),
]
url_api = [
    path("api/status_on", view.views_sessao.status_on, name="status_on"),
    path("api/status_off", view.views_sessao.status_off, name="status_off"),
    path(
        "api_cadastro_clientes",
        view.views_cadastro.cadastro_empresa,
        name="api_cadastro_clientes",
    ),
    path("api_login", view.views_default.api_login, name="api_login"),  # funçoes js
    path("enviar-codigo/<str:email>", Utils.enviar_codigo, name="enviar_codigo"),
    path(
        "confirmar-codigo/<str:codigo>",
        Utils.confirmar_codigo,
        name="confirmar_codigo",
    ),
    path(
        "atualizar-senha/<str:nova_senha>",
        Utils.atualizar_senha,
        name="atualizar_senha",
    ),
    path("buscar_lojas", view.views_api.buscar_lojas, name="buscar_lojas"),
    path("endereco/create", view.views_api.create_endereco, name="create_endereco"),
    # Adicione outras URLs conforme necessário
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


urlpatterns2 = (
    url_api
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
    + url_erros
    + url_pdv
    + ur_personalizacao
)
