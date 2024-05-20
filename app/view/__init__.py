from .views_default import views_default
from .assinante import views_assinante
from .views_empresa import views_empresa
from .views_usuario import views_usuarios
from .views_loja import views_loja
from .views_produto import views_produto
from .views_venda import views_venda
from .views_cliente import views_cliente
from .views_galao import views_galao
from .views_endereco import views_endereco
from .views_motoboy import views_motoboy
from .views_configuracao import views_configuracao
from .sessao import views_sessao
from .views_cadastro import views_cadastro
from .views_empresa import views_empresa
from .views_autenticacao import views_autenticacao

# Definindo __all__ para expor todas as views de forma clara
__all__ = [
    "views_default",
    "views_assinante",
    "views_usuarios",
    "views_loja",
    "views_venda",
    "views_cliente",
    "views_galao",
    "views_api",
    "views_cadastro",
    "views_empresa",
    "views_endereco",
    "views_produto",
    "views_motoboy",
    "views_configuracao",
    "views_sessao",
    "views_autenticacao",
]
