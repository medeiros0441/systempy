from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.utils import Utils
from api.views import (
    PublicView,
    ClienteView,
    EmpresaView,
    UsuariosView,
    PersonalizacaoView,
    LojaView,
    ProdutoView,
    VendaView,
    GalaoView,
    EnderecoView,
    MotoboyView,
    ConfiguracaoView,
    SessaoView,
    ErroView,
    PdvView,
    TransacaoPdvView,
    AssociadoPdvView,
    RegistroDiarioPdvView,
)
from .TokenManager import TokenManager

# Configuração do roteador
router = DefaultRouter()
router.register(r'public', PublicView, basename='public')
router.register(r'clientes', ClienteView, basename='clientes')
router.register(r'empresas', EmpresaView, basename='empresas')
router.register(r'usuarios', UsuariosView, basename='usuarios')
router.register(r'personalizacao', PersonalizacaoView, basename='personalizacao')
router.register(r'lojas', LojaView, basename='lojas')
router.register(r'produtos', ProdutoView, basename='produtos')
router.register(r'vendas', VendaView, basename='vendas')
router.register(r'galoes', GalaoView, basename='galoes')
router.register(r'enderecos', EnderecoView, basename='enderecos')
router.register(r'motoboys', MotoboyView, basename='motoboys')
router.register(r'configuracoes', ConfiguracaoView, basename='configuracoes')
router.register(r'sessoes', SessaoView, basename='sessoes')
router.register(r'erros', ErroView, basename='erros')
router.register(r'pdvs', PdvView, basename='pdvs')
router.register(r'transacoes_pdvs', TransacaoPdvView, basename='transacoes_pdvs')
router.register(r'associados_pdvs', AssociadoPdvView, basename='associados_pdvs')
router.register(r'registros_diarios_pdvs', RegistroDiarioPdvView, basename='registros_diarios_pdvs')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('csrfToken/', TokenManager.csrf_token_view, name='csrfToken'),
    path('status_on/', SessaoView.status_on, name='status_on'),
    path('status_off/', SessaoView.status_off, name='status_off'),
]
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/some_path/", consumers.SomeConsumer.as_asgi()),
]