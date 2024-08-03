from django.contrib.auth.hashers import check_password, make_password
from ..TokenManager import TokenManager
from ..user import UserInfo
from .views_configuracao import views_configuracao
from random import choices
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from ..models import Usuario, Empresa
from ..utils import Utils
from ..gerencia_email.config_email import enviar_email


class views_public(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        try:
            data = request.data
            email = data.get("email", "").lower().strip()
            senha = data.get("senha", "")

            user = Usuario.objects.filter(email=email).first()
            if user:
                if check_password(senha, user.senha):
                    if not user.status_acesso:
                        return Response(
                            {
                                "message": "Usuário desativado. Entre em contato com o responsável da assinatura."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    user.utimo_login = timezone.now()
                    user.save()

                    payload = {
                        "id_usuario": str(user.id_usuario),
                        "id_empresa": str(user.empresa.id_empresa),
                        "nivel_usuario": user.nivel_usuario,
                        "status_acesso": user.status_acesso,
                    }

                    TokenManager.create_token(
                        nome_token="token_user", payload=payload, time=6
                    )

                    return Response(
                        {"success": True, "message": "Usuário logado com sucesso."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Credenciais inválidas. Tente novamente."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "O email não está cadastrado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"message": f"Erro interno durante a autenticação: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="check-auth")
    def check_authentication(self, request):
        print("cheou aqui")
        if UserInfo.is_authenticated(request):
            return Response({"authenticated": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"authenticated": False, "message": "Usuário não autenticado."},
                status=status.HTTP_403_FORBIDDEN,
            )

    @action(detail=False, methods=["post"], url_path="contact")
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

    @action(detail=False, methods=["post"], url_path="code/send")
    def send_code(self, request):
        try:
            email = request.data.get("email")
            if not email:
                return Response(
                    {"message": "Email não fornecido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            usuario = Usuario.objects.filter(email=email).first()
            if not usuario:
                return Response(
                    {"message": "Usuário não encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            codigo = (
                "".join(choices("0123456789", k=3))
                + "-"
                + "".join(choices("0123456789", k=3))
            )
            Utils.set_cookie(request, "codigo_autenticacao", codigo)
            Utils.set_cookie(request, "id_usuario", usuario.id_usuario)

            assunto = "Código de Recuperação de Senha"
            mensagem = f"Seu código de recuperação de senha é: {codigo}"
            enviar_email(
                destinatario=email,
                assunto=assunto,
                NomeCliente=usuario.primeiro_nome,
                TextIntroducao=mensagem,
            )

            return Response(
                {"message": "Código de recuperação enviado com sucesso."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": f"Erro interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"], url_path="code/confirm")
    def confirm_code(self, request):
        try:
            codigo = request.data.get("codigo")
            codigo_criptografado = Utils.get_cookie("codigo_autenticacao")
            if check_password(codigo, codigo_criptografado):
                return Response(
                    {"message": "Código confirmado com sucesso."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Código inválido. Tente novamente."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"message": f"Erro interno durante a autenticação: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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

            usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
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

        def verificar_existencia(campo, valor, funcao_verificadora):
            if funcao_verificadora(valor):
                mensagens_alerta.append(f"{campo} já cadastrado.")

        for campo, valor in campos.items():
            if campo == "E-mail":
                verificar_existencia(campo, valor, Utils.email_existe)
            elif campo == "Telefone":
                verificar_existencia(campo, valor, Utils.telefone_existe)
            elif campo == "CPF":
                verificar_existencia(campo, valor, Utils.cpf_existe)
            elif campo == "CNPJ":
                verificar_existencia(campo, valor, Utils.cnpj_existe)

        texto_alerta = "\n".join(mensagens_alerta)
        return texto_alerta.replace("\n", "\\n")

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        try:
            data = request.data

            email_responsavel = data.get("email_responsavel", "").lower().strip()
            dados_formulario = {
                "nome_empresa": data.get("nome_empresa"),
                "nro_cnpj": data.get("nro_cnpj"),
                "razao_social": data.get("razao_social_empresa"),
                "descricao": data.get("descricao_empresa"),
                "nome_responsavel": data.get("nome_responsavel"),
                "cargo": data.get("cargo_responsavel"),
                "email": email_responsavel,
                "nro_cpf": data.get("nro_cpf"),
                "telefone": data.get("telefone_responsavel"),
            }

            campos = {
                "E-mail": email_responsavel,
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
            if isinstance(empresa, Empresa):
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
            nova_empresa = Empresa.objects.create(**dados_empresa)
            return nova_empresa
        except Exception as e:
            return str(e)

    @staticmethod
    def create_user(empresa, senha):
        try:
            numero_aleatorio = Utils.gerar_numero_aleatorio()
            novo_nome_usuario = empresa.nome_responsavel + numero_aleatorio

            user_new = Usuario.objects.create(
                nome_completo=empresa.nome_responsavel,
                nome_usuario=novo_nome_usuario,
                senha=senha,
                nivel_usuario=1,
                status_acesso=True,
                email=empresa.email,
                empresa=empresa,
            )
            list = views_configuracao.list_configuracoes_padrao(user_new)
            views_configuracao.criar_configuracoes_padrao(list)
            return True
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            return str(e)
