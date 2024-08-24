# api/serializers/__init__.py
from .ClienteSerializer import ClienteSerializer
from .EntregaSerializer import EntregaSerializer,MotoboySerializer
from .LogSerializer import LogSerializer
from .CustomModelSerializer import CustomModelSerializer
from .GalaoSerializer import GalaoSerializer
from .LojaSerializer import LojaSerializer
from .SessaoSerializer import SessaoSerializer
from .EmpresaSerializer import EmpresaSerializer
from .HistoricoSerializer import HistoricoSerializer
from .PdvSerializer import PdvSerializer
from .UsuarioSerializer import UsuarioSerializer
from .EnderecoSerializer import EnderecoSerializer
from .ProdutoSerializer import ProdutoSerializer
from .VendaSerializer import VendaSerializer
__all__ = [
    "ClienteSerializer",
    "EntregaSerializer",
    "LogSerializer",
    "CustomModelSerializer",
    "GalaoSerializer",
    "LojaSerializer",
    "SessaoSerializer",
    "EmpresaSerializer",
    "HistoricoSerializer",
    "PdvSerializer",
    "UsuarioSerializer",
    "EnderecoSerializer",
    "ProdutoSerializer",
    "VendaSerializer",
    "MotoboySerializer"
]
