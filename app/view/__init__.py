from .views import home, cadastro, login, sobre, erro
from .assinante import home as a_home
from .views_empresa import (
    listar_empresas,
    criar_empresa,
    detalhes_empresa,
    editar_empresa,
    excluir_empresa,
)
from .views_usuario import (
    listar_usuarios,
    cadastrar_usuario,
    detalhes_usuario,
    excluir_usuario,
    ativar_usuario,
    bloquear_usuario,
    editar_usuario,
)
from .views_loja import (
    lista_lojas,
    editar_loja,
    selecionar_loja,
    excluir_loja,
    criar_loja,
)
from .views_produto import (
    lista_produtos,
    criar_produto,
    editar_produto,
    selecionar_produto,
    excluir_produto,
    acrescentar_produto,
)
from .views_venda import (
    lista_vendas,
    editar_venda,
    selecionar_venda,
    excluir_venda,
)
from .views_cliente import (
    lista_clientes,
    criar_cliente,
    editar_cliente,
    selecionar_cliente,
    excluir_cliente,
)
from .views_galao import (
    lista_galao,
    editar_galao,
    selecionar_galao,
    excluir_galao,
)
from .views_endereco import (
    criar_endereco,
    lista_enderecos,
    selecionar_endereco,
    editar_endereco,
    delete_endereco,
)

from .view_configuracao import (
    ConfiguracaoCreateView,
    ConfiguracaoDeleteView,
    ConfiguracaoDetailView,
    ConfiguracaoListView,
    ConfiguracaoUpdateView,
)
