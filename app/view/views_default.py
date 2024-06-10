from django.shortcuts import render, redirect
from django.utils import timezone
from .views_autenticacao import views_autenticacao
from ..gerencia_email.config_email import enviar_email
from app.static import Alerta, UserInfo
from .views_erro import views_erro
from app.utils import Utils
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied


class views_default:

    def home(request, context=None):
        id_empresa = UserInfo.get_id_empresa(request)
        id_usuario = UserInfo.get_id_usuario(request)

        if context is None:
            context = {}

        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = Utils.criar_alerta_js(alerta)

        return render(request, "default/home.html", context)

    def sobre(request):

        if request.method == "POST":
            try:
                # Obter os dados do formulário POST
                nome = request.POST.get("txtNome")
                telefone = request.POST.get("txtTelefone")
                email = request.POST.get("txtEmail")
                mensagem = request.POST.get("txtMensagem")

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

                return render(
                    request,
                    "default/sobre.html",
                    {"alerta_js": Utils.criar_alerta_js("Mensagem Enviada.")},
                )
            except Exception as e:
                mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)
        else:
            return render(request, "default/sobre.html")

    def cadastro(request):
        try:
            return render(request, "default/cadastro.html")

        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)

    @csrf_exempt
    def api_login(request):
        try:
            response_data = {}
            if request.method == "POST":
                data = json.loads(request.body)
                email = data.get("email", "").lower().strip()
                senha = data.get("senha", "")
                valor_checkbox = data.get("flexCheckDefault")

                if valor_checkbox == "on":
                    request.session["email_saved"] = email
                    request.session["senha_saved"] = senha
                    request.session["checkbox_login"] = "on"
                else:
                    request.session["email_saved"] = None
                    request.session["senha_saved"] = None
                    request.session["checkbox_login"] = None
                status, mensagem = views_autenticacao.autenticar_usuario(
                    request, email, senha
                )
                if status:
                    response_data["success"] = True
                    response_data["redirect_url"] = "/dashboard"
                else:
                    response_data["success"] = False
                    response_data["message"] = mensagem

            elif request.session.get("checkbox_login") == "on":
                email_saved = request.session.get("email_saved")
                senha_saved = request.session.get("senha_saved")
                if email_saved and senha_saved:
                    if views_autenticacao.autenticar_usuario(
                        request, email_saved, senha_saved
                    ):
                        response_data["success"] = True
                        response_data["redirect_url"] = "/dashboard"

            return JsonResponse(response_data)

        except Exception as e:
            # Se ocorrer um erro inesperado, retorne uma resposta de erro JSON
            return JsonResponse(
                {"message": f"Erro durante o login: {str(e)}"}, status=500
            )

    def login(request, context={}):
        try:
            # Verifica se há alerta e adiciona ao contexto, se houver
            alerta = Alerta.get_mensagem()
            if alerta:
                context["alerta_js"] = Utils.criar_alerta_js(alerta)

            email_saved = request.session.get("email_saved")
            senha_saved = request.session.get("senha_saved")
            checkbox_login = request.session.get("checkbox_login")

            if email_saved is not None:
                context["email_saved"] = email_saved
            if senha_saved is not None:
                context["senha_saved"] = senha_saved
            if checkbox_login is not None:
                context["checkbox_login"] = checkbox_login

            # Renderiza a página de login com o contexto atualizado
            return render(request, "default/login.html", context)

        except Exception as e:
            # Se ocorrer um erro inesperado, redireciona para a página de erro
            return views_erro.erro(request, f"Erro durante o login: {str(e)}")
