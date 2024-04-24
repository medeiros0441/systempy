from .views import home, cadastro, login, sobre, erro
from .assinante import views_assinante
from .views_empresa import (
    listar_empresas,
    criar_empresa,
    detalhes_empresa,
    editar_empresa,
    excluir_empresa,
)
from .views_usuario import view_usuarios
from .views_loja import (
    lista_lojas,
    editar_loja,
    selecionar_loja,
    excluir_loja,
    criar_loja,
)
from .views_produto import views_produto
from .views_venda import views_venda
from .views_cliente import views_cliente
from .views_galao import views_galao
from .views_endereco import views_endereco
from .views_motoboy import views_motoboy

from .view_configuracao import (
    ConfiguracaoCreateView,
    ConfiguracaoDeleteView,
    ConfiguracaoDetailView,
    ConfiguracaoListView,
    ConfiguracaoUpdateView,
)
from .sessao import (
    sessao_usuario_list,
    sessao_usuario_detail,
    sessao_usuario_delete,
    atualizar_sessao_usuario,
    status_on,
    status_off,
    get_sessao_usuario,
    criar_sessao,
)
