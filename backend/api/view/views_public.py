from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from ..models import Empresa, Usuario
from ..gerencia_email.config_email import enviar_email
from api.utils import Utils
from ..TokenManager import TokenManager
from ..user import UserInfo
from .views_configuracao import views_configuracao
from random import choices
from django.views.decorators.csrf import csrf_exempt, csrf_protect


class views_public:

    
    @api_view(["GET"])
    def check_authentication(request):
        if UserInfo.is_authenticated(request):
            return Response({"authenticated": True}, status=200)
        else:
            return Response(
                {"authenticated": False, "message": "Usuário não autenticado."},
                status=403,
            )

    
    @api_view(["POST"])
    def contato(request):
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

            return Response({"message": "Mensagem Enviada."}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    
    @api_view(["POST"])
    def SetLogin(request):
        try:
            data = request.data
            email = data.get("email", "").lower().strip()
            senha = data.get("senha", "")

            usuario = Usuario.objects.filter(email=email).first()
            if usuario:
                senha_correta = check_password(senha, usuario.senha)
                if senha_correta:
                    if not usuario.status_acesso:
                        return Response(
                            {
                                "message": "Usuário desativado. Entre em contato com o responsável da assinatura"
                            },
                            status=400,
                        )
                    usuario.utimo_login = timezone.now()
                    usuario.save()

                    payload = {
                        "id_usuario": str(usuario.id_usuario),
                        "id_empresa": str(usuario.empresa.id_empresa),
                        "nivel_usuario": usuario.nivel_usuario,
                        "status_acesso": usuario.status_acesso,
                    }

                    TokenManager.create_token(
                        nome_token="token_user",
                        payload=payload,
                        time=6,
                    )

                    return Response(
                        {"success": True, "message": "Usuário logado com sucesso."},
                        status=200,
                    )
                else:
                    return Response(
                        {"message": "Credenciais inválidas. Tente novamente."},
                        status=400,
                    )
            else:
                return Response({"message": "O email não está cadastrado."}, status=400)
        except Exception as e:
            return Response(
                {"message": f"Erro interno durante a autenticação: {str(e)}"},
                status=500,
            )

    
    @api_view(["POST"])
    def enviar_codigo(request, email):
        try:
            if not email:
                return Response({"message": "Email não fornecido."}, status=400)

            usuario = Usuario.objects.filter(email=email).first()
            if not usuario:
                return Response({"message": "Usuário não encontrado."}, status=404)

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
                status=200,
            )

        except Exception as e:
            return Response({"message": f"Erro interno: {str(e)}"}, status=500)

    
    @api_view(["POST"])
    def confirmar_codigo(request, codigo):
        try:
            codigo_criptografado = Utils.get_cookie("codigo_autenticacao")
            if check_password(codigo, codigo_criptografado):
                return Response(
                    {"message": "Código confirmado com sucesso."}, status=200
                )
            else:
                return Response(
                    {"message": "Código inválido. Tente novamente."}, status=400
                )
        except Exception as e:
            return Response(
                {"message": f"Erro interno durante a autenticação: {str(e)}"},
                status=500,
            )

    
    @api_view(["POST"])
    def atualizar_senha(request):
        try:
            data = request.data
            senha_nova = data.get("senha_nova", "")

            id_usuario = Utils.get_cookie("id_usuario")
            if not id_usuario:
                return Response({"message": "Usuário não autenticado."}, status=403)

            usuario = Usuario.objects.filter(id_usuario=id_usuario).first()
            if not usuario:
                return Response({"message": "Usuário não encontrado."}, status=404)

            if not senha_nova:
                return Response({"message": "Campo senha está vazio."}, status=400)

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

            return Response({"message": "Operação concluída com sucesso."}, status=200)

        except Exception as e:
            return Response(
                {"message": f"Erro durante a recuperação de senha: {str(e)}"},
                status=500,
            )

    
    def validacao(campos):
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

    
    @api_view(["POST"])
    def cadastro(request):
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

            mensagens_alerta = views_public.validacao(campos)
            if mensagens_alerta:
                return Response(
                    {"success": False, "message": mensagens_alerta}, status=400
                )

            senha = data.get("senha")
            if not senha:
                return Response(
                    {"success": False, "message": ["Campo senha está vazio"]},
                    status=400,
                )

            senha_hash = make_password(senha)
            empresa = views_public.criar_empresa(dados_formulario)
            if isinstance(empresa, Empresa):
                string_value = views_public.criar_user(empresa, senha_hash)
                if string_value is True:
                    return Response({"success": True, "redirect": "login"}, status=200)
                else:
                    return Response(
                        {"success": False, "message": [string_value]}, status=400
                    )
            else:
                return Response(
                    {"success": False, "message": ["Erro ao criar empresa"]}, status=400
                )
        except Exception as e:
            return Response({"success": False, "message": [str(e)]}, status=500)

    
    def criar_empresa(dados_empresa):
        try:
            nova_empresa = Empresa.objects.create(**dados_empresa)
            return nova_empresa
        except Exception as e:
            return str(e)

    
    def criar_user(empresa, senha):
        try:
            numero_aleatorio = Utils.gerar_numero_aleatorio()
            novo_nome_usuario = empresa.nome_responsavel + numero_aleatorio

            novo_usuario = Usuario.objects.create(
                nome_completo=empresa.nome_responsavel,
                nome_usuario=novo_nome_usuario,
                senha=senha,
                nivel_usuario=1,
                status_acesso=True,
                email=empresa.email,
                empresa=empresa,
            )
            list = views_configuracao.list_configuracoes_padrao(novo_usuario)
            views_configuracao.criar_configuracoes_padrao(list)
            return True
        except Exception as e:
            print(f"Erro ao criar usuário: {str(e)}")
            return str(e)
