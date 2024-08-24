# services.py
from api.models import EmpresaModel, ConfiguracaoModel
from api.utils import Utils
from django.core.exceptions import ObjectDoesNotExist

class EmpresaService:

    @staticmethod
    def get_all_empresas():
        return EmpresaModel.objects.all()

    @staticmethod
    def get_empresa_by_id(id):
        return EmpresaModel.objects.get(pk=id)

    @staticmethod
    def create_empresa(data):
        return EmpresaModel.objects.create(
            nome_empresa=data["nome_empresa"],
            nro_cnpj=data["nro_cnpj"],
            razao_social=data.get("razao_social"),
            descricao=data.get("descricao"),
            nome_responsavel=data["nome_responsavel"],
            cargo=data["cargo"],
            email=data["email"],
            nro_cpf=data["nro_cpf"],
            telefone=data["telefone"],
        )

    @staticmethod
    def update_empresa(id, data):
        empresa = EmpresaModel.objects.get(pk=id)
        for field, value in data.items():
            setattr(empresa, field, value)
        empresa.save()
        return empresa

    @staticmethod
    def delete_empresa(id):
        empresa = EmpresaModel.objects.get(pk=id)
        empresa.delete()
        return empresa

    @staticmethod
    def telefone_existe(telefone):
        return EmpresaModel.objects.filter(telefone__iexact=telefone).exists()

    @staticmethod
    def cpf_existe(cpf):
        return EmpresaModel.objects.filter(nro_cpf__iexact=cpf).exists()

    @staticmethod
    def cnpj_existe(cnpj):
        return EmpresaModel.objects.filter(nro_cnpj__iexact=cnpj).exists()
