from django.contrib.auth.hashers import check_password, make_password
from ..TokenManager import TokenManager
from ..user import UserInfo
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from api.models import UsuarioModel, EmpresaModel
from ..utils import Utils
from ..gerencia_email.config_email import enviar_email
from api.services import EmpresaService,UsuarioService
  
class PublicView(viewsets.ViewSet):
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
            if not user.status_acesso:
                return Response(
                    {"message": "Usuário desativado. Entre em contato com o responsável da assinatura."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            user.utimo_login = timezone.now()
            user.save()
            payload = {
                "id_usuario": str(user.id_usuario),
                "id_empresa": str(user.empresa.id_empresa),
                "nivel_usuario": user.nivel_usuario,
                "status_acesso": user.status_acesso,
            }
            token = TokenManager.create_token(payload=payload, time=6)
            response = Response(
                {"success": True, "message": "Usuário logado com sucesso."},
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                key="user_token",
                value=token,
                httponly=True,  # valor variável conforme necessidade
                secure=True,    # Use True se estiver usando HTTPS
                samesite="Strict",  # Adicione mais segurança ao cookie
            )
            return response
        except Exception as e:
            # Registro do erro para depuração
            return Response(
                {"message": f"Erro interno durante a autenticação. {str(e)}" },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    @action(detail=False, methods=["get"], url_path="check-auth")
    def check_authentication(self, request):
        status,message =UserInfo.is_authenticated(request)
        print(status)
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
    
    def send_recovery_code(email, nome, assunto=None, mensagem=None):
        """
        Envia um código de recuperação para o e-mail fornecido.
        """
        hash, codigo = Utils.generate_code()
        mensagem_completa = f"{mensagem} {codigo}"

        response = Response(
            {"message": "Código enviado com sucesso."},
            status=status.HTTP_200_OK
        )
        Utils.set_cookie(response,"codigo_hasher", hash)

        enviar_email(
            destinatario=email,
            assunto=assunto or "Recuperação de Senha",
            NomeCliente=nome or '',
            TextIntroducao=mensagem_completa
        )

        return response

    @action(detail=False, methods=["post"], url_path="code/send/password")
    def send_password_code(self, request):
        """Envia um código de recuperação de senha para o email fornecido."""
        try:
            email = request.data.get("email")
            if not email:
                return Response({"message": "Email não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

            usuario = UsuarioService.verificar_email(email, True)
            if not usuario['id_usuario'] and usuario['email']:
                return Response({"message": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
            nome_completo = usuario.get('nome_completo', 'Usuário')
            mensagem = f"Olá, {nome_completo}. O seu código para recuperar a senha é:"
            assunto = "Recuperação de Senha"
            response = PublicView.send_recovery_code(email, nome_completo, assunto, mensagem)
            Utils.set_cookie(response, "password_analise", {"id_usuario": usuario['id_usuario'], "email": usuario['email']})
    
            return response
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Erro interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"], url_path="code/send")
    def send_code(self, request):
        """Envia um código de confirmação para o email e nome fornecidos."""
        try:
            email = request.data.get("email")
            nome = request.data.get("nome")
            if not email:
                return Response({"message":"Email não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

            if not nome:
                    nome = ""
            assunto = "Confirmação de Email"
            mensagem = f"Olá, {nome}. Esse é o código para a confirmação de seu email."
            return PublicView.send_recovery_code(email, nome, assunto, mensagem)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": f"Erro interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"], url_path="code/confirm")
    def confirm_code(self, request):
        """Confirma o código de recuperação fornecido."""
        try:
            codigo = request.data.get("codigo")
            codigo_criptografado = Utils.get_cookie(request, "codigo_hasher")
            
            if not codigo_criptografado:
                return Response(
                    {"message": "Código de recuperação não encontrado, Tente iniciar o processo novamente."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if check_password(codigo, codigo_criptografado):
                response = Response(
                    {"message": "Código confirmado com sucesso.", "is_valido": True},
                    status=status.HTTP_200_OK,
                )
                data = Utils.get_cookie(request,"password_analise")
                Utils.set_cookie(response,"password_confirmado", {"id_usuario": data['id_usuario'], "email": data['email']})
                
                return response
            else:
                return Response(
                    {"message": "Código inválido. Tente novamente.", "is_valido": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"message": f"Erro interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
    @action(detail=False, methods=["post"], url_path="password/update")
    def update_password(self, request):
        try:
            senha_nova = request.data.get("senha")
            data = Utils.get_cookie(request,"password_confirmado")
            id_usuario = data['id_usuario']
            email =  data['email']
            if not id_usuario and email:
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
                NomeCliente=usuario.nome_completo,
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

        # Juntar todas as mensagens com uma quebra de linha adequada
        texto_alerta = "\n".join(mensagens_alerta)
        
        # Retornar o texto com quebras de linha como '\n'
        return texto_alerta

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
                "email": data.get("email_responsavel", "").lower().strip(),
                "nro_cpf": data.get("nro_cpf"),
                "telefone": data.get("telefone_responsavel"),
            }

            # Validação dos campos críticos
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

            # Processar a criação da empresa e do usuário
            success, message = EmpresaService.create_company_and_user(dados_formulario, senha)
            if success:
                enviar_email(
                    destinatario=dados_formulario.get("email"),
                    assunto="Cadastro Concluído com sucesso",
                    NomeCliente=dados_formulario.get("nome_responsavel"),
                    TextIntroducao="Olá! Seja bem-vindo. Sua conta já está disponível para uso. :)"
                )
                return Response(
                    {"success": True, "redirect": "login"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"success": False, "message": [message]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"success": False, "message": [str(e)]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

     