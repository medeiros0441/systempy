from ..gerencia_email.config_email import enviar_email
from api.utils import Utils
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from random import choices
from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.contrib.auth.hashers import check_password, make_password
from ..models import Empresa, Usuario
from .views_configuracao import views_configuracao
from django.utils import timezone
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ..static import UserInfo
from ..TokenManager import TokenManager
class views_public(APIView):
    permission_classes = [AllowAny]

    def check_authentication(request):
        if UserInfo.is_authenticated(request):
            return JsonResponse({'authenticated': True}, status=200)
        else:
            return JsonResponse({'authenticated': False, 'message': "Usuário não autenticado."}, status=403)
        
    @csrf_exempt
    def contato(request):

        if request.method == "POST":
            try:
                # Obter os dados do formulário POST
                data = json.loads(request.body)
                nome = data.get("nome")
                telefone = data.get("telefone")
                email = data.get("email")
                mensagem = data.get("mensagem")

                # Construir a mensagem do e-mail
                mensagem_modelo = (
                    f"Contato via Site\n"
                    f"Nome: {nome}\n"
                    f"WhatsApp: {telefone}\n"
                    f"E-mail: {email}\n"
                )

                # Enviar o # Enviar o e-mail para o destinatário
                enviar_email(
                    destinatario="medeiros0442@gmail.com",
                    assunto="Contato via site CPS",
                    NomeCliente=nome,
                    TextIntroducao=mensagem_modelo,
                    TextContainer2=mensagem,
                )

                # Retornar uma resposta JSON de sucesso
                return JsonResponse({"message": "Mensagem Enviada."}, status=200)

            except Exception as e:
                mensagem_erro = str(e)
                # Retornar uma resposta JSON de erro
                return JsonResponse({"error": mensagem_erro}, status=500)

        # Caso não seja uma requisição POST, retornar um erro 405 Método Não Permitido
        return JsonResponse({"error": "Método não permitido"}, status=405)

    
    @csrf_exempt
    def SetLogin(request):
        try:
            if request.method == "POST":
                data = json.loads(request.body)
                email = data.get("email", "").lower().strip()
                senha = data.get("senha",  "")
                # Verifica se o usuário existe
                usuario = Usuario.objects.filter(email=email).first()
                if usuario:
                    senha_correta = check_password(senha, usuario.senha)
                    if senha_correta:
                        if not usuario.status_acesso:
                            return JsonResponse(
                                {
                                    "message": "Usuário desativado. Entre em contato com o responsável da assinatura"
                                },
                                status=400,
                            )
                        # Atualiza o último login do usuário
                        usuario.ultimo_login = timezone.now()
                        usuario.save()

                        # Gera o token JWT usando o método create_token
                        payload = {
                            "id_usuario": str(usuario.id_usuario),
                            "id_empresa": str(usuario.empresa.id_empresa),
                            "nivel_usuario": usuario.nivel_usuario,
                            "status_acesso": usuario.status_acesso
                        }
                        
                        response = TokenManager.create_token(
                            nome_token="jwt_token",
                            payload=payload,
                            time=24,  # Expiração em horas
                            httponly=False  # pode ser variável
                        )

                        return response
                    else:
                        return JsonResponse(
                            {"message": "Credenciais inválidas. Tente novamente."},
                            status=400,
                        )
                else:
                    return JsonResponse(
                        {"message": "O email não está cadastrado."}, status=400
                    )
        except Exception as e:
            error_message = f"Erro interno durante a autenticação: {str(e)}."
            return JsonResponse({"message": error_message}, status=500)

    @csrf_exempt
    def enviar_codigo(request, email):
        try:
            if request.method == "POST":
                if not email:
                    return JsonResponse({"message": "Email não fornecido."}, status=400)
                try:
                    # Verificar se o usuário com o e-mail fornecido existe no banco de dados
                    usuario = Usuario.objects.get(email=email)

                    # Gerar um número com 6 dígitos
                    codigo = (
                        "".join(choices("0123456789", k=3))
                        + "-"
                        + "".join(choices("0123456789", k=3))
                    )
                    make_password(codigo)
                    Utils.set_cookie(request, "codigo_autenticacao", codigo)
                    Utils.set_cookie(request, "id_usuario", usuario.id_usuario)

                    # Enviar o código para o e-mail do usuário
                    assunto = "Código de Recuperação de Senha"
                    mensagem = f"Seu código de recuperação de senha é: {codigo}"
                    enviar_email(
                        destinatario=email,
                        assunto=assunto,
                        NomeCliente=usuario.primeiro_nome,
                        TextIntroducao=mensagem,
                    )
                    return JsonResponse(
                        {"message": "Código de recuperação enviado com sucesso."},
                        status=200,
                    )

                except ObjectDoesNotExist:
                    return JsonResponse(
                        {"message": "Usuário não encontrado."}, status=404
                    )

        except Exception as e:
            return JsonResponse({"message": f"Erro interno: {str(e)}"}, status=500)

    @csrf_exempt
    def confirmar_codigo(request, codigo):
        try:
            codigo_criptografado = Utils.get_cookie("codigo_autenticacao")
            if check_password(codigo, codigo_criptografado):
                return JsonResponse(
                    {"message": "Código confirmado com sucesso."}, status=200
                )
            else:
                return JsonResponse(
                    {"message": "Código inválido. Tente novamente."}, status=400
                )
        except Exception as e:
            error_message = f"Erro interno durante a autenticação: {str(e)}."
            return JsonResponse({"message": error_message}, status=500)

    @csrf_exempt
    def atualizar_senha(request):
        try:
            if request.method == "POST":
                data = json.loads(request.body)
                senha_nova = data.get("senha_nova", "")

                id_usuario = Utils.get_cookie("id_usuario")
                if not id_usuario:
                    return JsonResponse(
                        {"message": "Usuário não autenticado."}, status=403
                    )

                usuario = Usuario.objects.filter(id_usuario=id_usuario).first()

                if usuario:
                    if not senha_nova:
                        return JsonResponse(
                            {"message": "Campo senha está vazio."}, status=400
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

                    return JsonResponse(
                        {"message": "Operação concluída com sucesso."}, status=200
                    )
                else:
                    return JsonResponse(
                        {"message": "Usuário não encontrado."}, status=404
                    )

        except Exception as e:
            return JsonResponse(
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
        return texto_alerta.replace("\n", "\\n")  # Substituir quebras de linha por '\n'

    @csrf_exempt
    def cadastro(request):
        try:
            if request.method == "POST":
                data = json.loads(request.body)

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
                mensagens_alerta = []

                campos = {
                    "E-mail": email_responsavel,
                    "Telefone": dados_formulario.get("telefone"),
                    "CPF": dados_formulario.get("nro_cpf"),
                    "CNPJ": dados_formulario.get("nro_cnpj"),
                }

                mensagens_alerta = views_public.validacao(campos)
                if mensagens_alerta:
                    return JsonResponse(
                        {"success": False, "message": mensagens_alerta}, status=400
                    )

                senha = data.get("senha")
                if not senha:
                    return JsonResponse(
                        {"success": False, "message": ["Campo senha está vazio"]},
                        status=400,
                    )

                senha_hash = make_password(senha)
                empresa = views_public.criar_empresa(dados_formulario)
                if empresa:
                    string_value = views_public.criar_user(empresa, senha_hash)
                    if string_value is True:
                        return JsonResponse({"success": True, "redirect": "login"})
                    else:
                        return JsonResponse(
                            {"success": False, "message": [string_value]}, status=400
                        )
                else:
                    return JsonResponse(
                        {"success": False, "message": ["Erro ao criar empresa"]},
                        status=400,
                    )
            else:
                return JsonResponse(
                    {"success": False, "message": ["Método não permitido"]}, status=405
                )
        except Exception as e:
            return JsonResponse({"success": False, "message": [str(e)]}, status=500)

    def criar_empresa(dados_empresa):
        try:
            nova_empresa = Empresa.objects.create(**dados_empresa)
            print(nova_empresa)
            return nova_empresa
        except Exception as e:
            mensagem_erro = str(e)
            return mensagem_erro

    def criar_user(empresa, senha):
        # Criação do novo usuário associado à empresa
        # Retorna True se o usuário foi criado com sucesso, False caso contrário
        try:
            numero_aleatorio = Utils.gerar_numero_aleatorio()
            novo_nome_usuario = empresa.nome_responsavel + numero_aleatorio

            # Criando o novo usuário associado à empresa
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
            mensagem_erro = str(e)
            print(
                "Erro ao criar usuário:", mensagem_erro
            )  # Adiciona mensagem de depuração
            return mensagem_erro
