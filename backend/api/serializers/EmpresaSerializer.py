from api.models import EmpresaModel
from .CustomModelSerializer import  CustomModelSerializer

class EmpresaSerializer(CustomModelSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = EmpresaModel
        fields = CustomModelSerializer.Meta.fields + [
            'id_empresa',
            'nome_empresa',
            'nro_cnpj',
            'razao_social',
            'descricao',
            'nome_responsavel',
            'cargo',
            'email',
            'nro_cpf',
            'telefone',
        ]
