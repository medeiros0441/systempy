# serializers.py
from rest_framework import serializers
from models.usuario import Usuario, Personalizacao
from models.empresa import Empresa
from models.endereco import Endereco
from models.galao import Galao, GestaoGalao
from models.loja import Loja, Associado
from models.produto import Produto
from models.sessao import Sessao
from models.venda import Venda, ItemCompra, Motoboy, Entrega
from models.pdv import PDV, TransacaoPDV, AssociadoPDV, RegistroDiarioPDV
from models.historico import Historico, HistoricoAlteracoes
from models.log import Log
from models.configuracao import Configuracao
from models.cliente import Cliente
from models.CustomModel import CustomModel


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"


class PersonalizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalizacao
        fields = "__all__"


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = "__all__"


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = "__all__"


class GalaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galao
        fields = "__all__"


class GestaoGalaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestaoGalao
        fields = "__all__"


class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = "__all__"


class AssociadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Associado
        fields = "__all__"


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"


class SessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessao
        fields = "__all__"


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = "__all__"


class ItemCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = "__all__"


class MotoboySerializer(serializers.ModelSerializer):
    class Meta:
        model = Motoboy
        fields = "__all__"


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = "__all__"


class PDVSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDV
        fields = "__all__"


class TransacaoPDVSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransacaoPDV
        fields = "__all__"


class AssociadoPDVSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociadoPDV
        fields = "__all__"


class RegistroDiarioPDVSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroDiarioPDV
        fields = "__all__"


class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = "__all__"


class HistoricoAlteracoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoAlteracoes
        fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"


class ConfiguracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracao
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
