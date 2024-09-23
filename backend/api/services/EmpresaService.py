# services.py
from api.models import EmpresaModel, ConfiguracaoModel, UsuarioModel
from api.utils import Utils
from django.core.exceptions import ObjectDoesNotExist
from .ConfiguracaoService import ConfiguracaoService
class EmpresaService:

    @staticmethod
    def get_all_empresas():
        return EmpresaModel.objects.all()

    @staticmethod
    def get_empresa_by_id(id):
        return EmpresaModel.objects.get(pk=id)
    
    @staticmethod
    def get_exist_empresa(id_empresa, return_data=False):
        """
        Verifica se uma empresa já existe com base no ID.
        
        Args:
            id_empresa (int): ID da empresa.
            return_data (bool): Se True, retorna os dados da empresa; se False, retorna apenas um valor booleano.
        
        Returns:
            EmpresaModel | bool: Dados da empresa ou um valor booleano indicando a existência.
        """
        try:
            # Busca a empresa pelo ID
            empresa = EmpresaModel.objects.filter(pk=id_empresa).first()

            if empresa and return_data:
                return empresa  # Retorna a empresa se encontrada e 'return_data' for True
            return bool(empresa)  # Retorna True/False se a empresa foi encontrada ou não

        except Exception as e:
            # Em caso de erro, logue a exceção se necessário e retorne False
            return False
 
    @staticmethod
    def create_empresa(data):
        """
        Cria uma nova empresa no banco de dados.
        
        Args:
            data (dict): Dicionário contendo os dados da empresa.
        
        Returns:
            EmpresaModel | str: Instância da empresa criada ou string de erro.
        """
        try:
            nova_empresa = EmpresaModel.objects.create(
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
            return nova_empresa
        except Exception as e:
            return str(e)

    @staticmethod
    def create_user(empresa, senha):
        """
        Cria um novo usuário associado à empresa no banco de dados.
        
        Args:
            empresa (EmpresaModel): Instância da empresa criada.
            senha (str): Senha do usuário responsável.
        
        Returns:
            bool | str: True se o usuário for criado com sucesso, ou string de erro.
        """
        try:
            numero_aleatorio = Utils.gerar_numero_aleatorio()
            novo_nome_usuario = empresa.nome_responsavel + numero_aleatorio

            user_new = UsuarioModel.objects.create(
                nome_completo=empresa.nome_responsavel,
                nome_usuario=novo_nome_usuario,
                senha=senha,
                nivel_usuario=1,
                status_acesso=True,
                email=empresa.email,
                empresa=empresa,
            )

            # Criar configurações padrão para o usuário
            configuracoes_padrao = ConfiguracaoService.list_configuracoes_padrao(user_new)
            ConfiguracaoService.criar_configuracoes_padrao(configuracoes_padrao)

            return True
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            return str(e)

    @staticmethod
    def create_company_and_user(dados_empresa, senha):
        """
        Executa o processo de criação de uma empresa e do usuário associado.
        
        Args:
            dados_empresa (dict): Dicionário contendo os dados da empresa.
            senha (str): Senha do usuário responsável.
        
        Returns:
            tuple: Um tupla contendo (success, message).
                   success (bool): Indica se o processo foi bem-sucedido.
                   message (str): Mensagem de erro em caso de falha ou sucesso.
        """
        try:
            # Criar empresa
            nova_empresa = EmpresaService.create_empresa(dados_empresa)
            if not isinstance(nova_empresa, EmpresaModel):
                return False, f"Erro ao criar empresa: {nova_empresa}"

            # Criar usuário associado à empresa
            result = EmpresaService.create_user(nova_empresa, senha)
            if result is not True:
                return False, f"Erro ao criar usuário: {result}"

            return True, "Empresa e usuário criados com sucesso."
        except Exception as e:
            return False, f"Erro no processo de criação: {str(e)}"
        
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
