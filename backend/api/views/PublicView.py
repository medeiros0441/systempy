from django.contrib.auth.hashers import check_password, make_password
from ..TokenManager import TokenManager
from ..user import UserInfo
from .ConfiguracaoView import ConfiguracaoView
from random import choices
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from models import UsuarioModel, EmpresaModel
from ..utils import Utils
from ..gerencia_email.config_email import enviar_email

from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

def generate_code():
    """Gera um código de recuperação e o criptografa."""
    code = f"{get_random_string(length=3, allowed_chars='0123456789')}-{get_random_string(length=3, allowed_chars='0123456789')}"
    return make_password(code) ,code #

def handle_exception(e):
    """Retorna uma resposta de erro com uma mensagem interna."""
    return Response(
        {"message": f"Erro interno: {str(e)}"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

class ViewsPublic(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        try:
            # Obtém os dados da requisição
            data = request.data
            email = data.get("email", "").lower().strip()
            senha = data.get("senha", "")

            # Valida se os campos obrigatórios estão presentes
            if not email or not senha:
                return Response(
                    {"message": "Email e senha são obrigatórios."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                # Busca o usuário pelo email
                user = UsuarioModel.objects.get(email=email)
            except UsuarioModel.DoesNotExist:
                return Response(
                    {"message": "O email não está cadastrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Verifica a senha
            if not check_password(senha, user.senha):
                return Response(
                    {"message": "Credenciais inválidas. Tente novamente."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Verifica o status do usuário
            if not user.status_acesso:
                return Response(
                    {"message": "Usuário desativado. Entre em contato com o responsável da assinatura."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Atualiza o último login e salva
            user.utimo_login = timezone.now()
            user.save()

            # Cria o token e o retorna
            payload = {
                "id_usuario": str(user.id_usuario),
                "id_empresa": str(user.empresa.id_empresa),
                "nivel_usuario": user.nivel_usuario,
                "status_acesso": user.status_acesso,
            }

            token = TokenManager.create_token(nome_token="user_token", payload=payload, time=6, httponly=True)

            return Response(
                {"success": True, "message": "Usuário logado com sucesso.", "token": token},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Registro do erro para depuração
            return Response(
                {"message": "Erro interno durante a autenticação."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    @action(detail=False, methods=["get"], url_path="check-auth")
    def check_authentication(self, request):
        status,message =UserInfo.is_authenticated(request)
        return Response({"authenticated": status, "message":message},
            status=200,
        )

    @action(detail=False, methods=["post"], url_path="contato")
    def contact(self, request):
        try:
            data = request.data
            nome = data.get("nome")
            telefone = data.get("telefone")
            email = data.get("email")
            mensagem = data.get("mensagem")

            mensagem_modelo = (
                f"Contato via Site\n"
                f"Nome: {nome}\n"
                f"WhatsApp: {telefone}\n"
                f"E-mail: {email}\n"
            )

            enviar_email(
                destinatario="medeiros0442@gmail.com",
                assunto="Contato via site CPS",
                NomeCliente=nome,
                TextIntroducao=mensagem_modelo,
                TextContainer2=mensagem,
            )

            return Response({"message": "Mensagem Enviada."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
    def validate_email(email):
        if not email:
            raise ValueError("Email não fornecido.")

    def handle_user_not_found():
        return Response(
            {"message": "Usuário não encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )

    def set_cookies(response, hash, usuario_id=None):
        max_age = 3600  # Define o tempo de vida do cookie para 1 hora (3600 segundos)
        
        response.set_cookie("codigo_hasher", hash, max_age=max_age)
        if usuario_id:
            response.set_cookie("id_usuario", usuario_id, max_age=max_age)
        
        return response

    def send_recovery_code(email, nome=None, usuario=None):
        hash, codigo = generate_code()
        assunto = "Código de Recuperação de Senha"
        mensagem = f"Seu código de recuperação de senha é: {codigo}"
        
        response = Response(
            {"message": "Código de recuperação enviado com sucesso."},
            status=status.HTTP_200_OK,
        )
        
        ViewsPublic.set_cookies(response, hash, usuario.id_usuario if usuario else None)

        enviar_email(
            destinatario=email,
            assunto=assunto,
            NomeCliente=nome if nome else usuario.primeiro_nome if usuario else '',
            TextIntroducao=mensagem,
        )
        
        return response

    @action(detail=False, methods=["post"], url_path="code/send/password")
    def send_password_code(self, request):
        """Envia um código de recuperação de senha para o email fornecido."""
        try:
            email = request.data.get("email")
            ViewsPublic.validate_email(email)

            usuario = UsuarioModel.objects.filter(email=email).first()
            if not usuario:
                return ViewsPublic.handle_user_not_found()

            return ViewsPublic.send_recovery_code(email, usuario=usuario)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_exception(e)

    @action(detail=False, methods=["post"], url_path="code/send")
    def send_code(self, request):
        """Envia um código de recuperação para o email e nome fornecidos."""
        try:
            email = request.data.get("email")
            nome = request.data.get("nome")
            ViewsPublic.validate_email(email)

            return ViewsPublic.send_recovery_code(email, nome=nome)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return handle_exception(e)

    @action(detail=False, methods=["post"], url_path="code/confirm")
    def confirm_code(self, request):
        """Confirma o código de recuperação fornecido."""
        try:
            codigo = request.data.get("codigo")
            codigo_criptografado = Utils.get_cookie(request, "codigo_hasher")
            
            if not codigo_criptografado:
                return Response(
                    {"message": "Código de recuperação não encontrado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if check_password(codigo, codigo_criptografado):
                return Response(
                    {"message": "Código confirmado com sucesso.", "is_valido": True},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Código inválido. Tente novamente.", "is_valido": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return handle_exception(e)
        
    @action(detail=False, methods=["post"], url_path="password/update")
    def update_password(self, request):
        try:
            senha_nova = request.data.get("senha_nova")
            id_usuario = Utils.get_cookie("id_usuario")
            if not id_usuario:
                return Response(
                    {"message": "Usuário não autenticado."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            usuario = UsuarioModel.objects.filter(id_usuario=id_usuario).first()
            if not usuario:
                return Response(
                    {"message": "Usuário não encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not senha_nova:
                return Response(
                    {"message": "Campo senha está vazio."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            senha_hash = make_password(senha_nova)
            usuario.senha = senha_hash
            usuario.save()

            assunto = "Senha Alterada"
            mensagem = "Sua senha foi alterada com sucesso."
            enviar_email(
                destinatario=usuario.email,
                assunto=assunto,
                NomeCliente=usuario.primeiro_nome,
                TextIntroducao=mensagem,
            )

            return Response(
                {"message": "Operação concluída com sucesso."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": f"Erro durante a recuperação de senha: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def validate_fields(campos):
        mensagens_alerta = []

        for campo, valor in campos.items():
            if campo == "E-mail":
                if not Utils.is_valid_email(valor):
                    mensagens_alerta.append(f"E-mail '{valor}' inválido.")
                elif UsuarioModel.objects.filter(email=valor).exists() or EmpresaModel.objects.filter(email=valor).exists():
                    mensagens_alerta.append(f"E-mail '{valor}' já cadastrado.")
            elif campo == "Telefone":
                if not Utils.is_valid_phone(valor):
                    mensagens_alerta.append(f"Telefone '{valor}' inválido.")
                elif EmpresaModel.objects.filter(telefone=valor).exists():
                    mensagens_alerta.append(f"Telefone '{valor}' já cadastrado.")
            elif campo == "CPF":
                if not Utils.is_valid_cpf(valor):
                    mensagens_alerta.append(f"CPF '{valor}' inválido.")
                elif EmpresaModel.objects.filter(nro_cpf=valor).exists():
                    mensagens_alerta.append(f"CPF '{valor}' já cadastrado.")
            elif campo == "CNPJ":
                if not Utils.is_valid_cnpj(valor):
                    mensagens_alerta.append(f"CNPJ '{valor}' inválido.")
                elif EmpresaModel.objects.filter(nro_cnpj=valor).exists():
                    mensagens_alerta.append(f"CNPJ '{valor}' já cadastrado.")

        texto_alerta = "\n".join(mensagens_alerta)
        return texto_alerta.replace("\n", "\\n")

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        try:
            data = request.data

            dados_formulario = {
                "nome_empresa": data.get("nome_empresa"),
                "nro_cnpj": data.get("nro_cnpj"),
                "razao_social": data.get("razao_social_empresa"),
                "descricao": data.get("descricao_empresa"),
                "nome_responsavel": data.get("nome_responsavel"),
                "cargo": data.get("cargo_responsavel"),
                "email":  data.get("email_responsavel", "").lower().strip(),
                "nro_cpf": data.get("nro_cpf"),
                "telefone": data.get("telefone_responsavel"),
            }

            campos = {
                "E-mail": dados_formulario.get("email"),
                "Telefone": dados_formulario.get("telefone"),
                "CPF": dados_formulario.get("nro_cpf"),
                "CNPJ": dados_formulario.get("nro_cnpj"),
            }

            mensagens_alerta = self.validate_fields(campos)
            if mensagens_alerta:
                return Response(
                    {"success": False, "message": mensagens_alerta},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            senha = data.get("senha")
            if not senha:
                return Response(
                    {"success": False, "message": ["Campo senha está vazio"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            senha_hash = make_password(senha)
            empresa = self.create_company(dados_formulario)
            if isinstance(empresa, EmpresaModel):
                result = self.create_user(empresa, senha_hash)
                if result is True:
                    return Response(
                        {"success": True, "redirect": "login"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"success": False, "message": [result]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"success": False, "message": ["Erro ao criar empresa"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"success": False, "message": [str(e)]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def create_company(dados_empresa):
        try:
            nova_empresa = EmpresaModel.objects.create(**dados_empresa)
            return nova_empresa
        except Exception as e:
            return str(e)

    @staticmethod
    def create_user(empresa, senha):
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
            list = ConfiguracaoView.list_configuracoes_padrao(user_new)
            ConfiguracaoView.criar_configuracoes_padrao(list)
            return True
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            return str(e)
