from django.shortcuts import render, redirect
from ..utils import utils
from django.utils import timezone
from .view_cadastro import cadastro_empresa
from .view_autenticacao import autenticar_usuario
from ..gerencia_email.config_email import enviar_email
from ..static import Alerta, UserInfo


class views_default:

    def home(request, context=None):
        id_empresa = UserInfo.get_id_empresa(request)
        id_usuario = UserInfo.get_id_usuario(request)

        if context is None:
            context = {}

        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = utils.criar_alerta_js(alerta)

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
                    {"alerta_js": utils.criar_alerta_js("Mensagem Enviada.")},
                )
            except Exception as e:
                mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)
        else:
            return render(request, "default/sobre.html")

    def cadastro(request):
        try:
            if request.method == "POST":
                return cadastro_empresa(request)
            else:
                return render(request, "default/cadastro.html")

        except Exception as e:
            mensagem_erro = str(e)
            return utils.erro(request, mensagem_erro)

    def login(request, context={}):
        try:
            alerta = Alerta.get_mensagem()
            if alerta:
                context["alerta_js"] = utils.criar_alerta_js(alerta)

            if request.method == "POST":
                # Se a requisição for POST, tenta obter os dados de email, senha e checkbox
                email = request.POST.get("email").lower().strip()
                senha = request.POST.get("senha")
                valor_checkbox = request.POST.get("flexCheckDefault")

                if valor_checkbox == "on":
                    request.session["email_saved"] = email
                    request.session["senha_saved"] = senha
                    request.session["checkbox_login"] = "on"
                else:
                    request.session["email_saved"] = None
                    request.session["senha_saved"] = None
                    request.session["checkbox_login"] = None

                # Chama a função para autenticar o usuário com os dados fornecidos
                if autenticar_usuario(request, email, senha):
                    return redirect("dashbord")
                else:
                    context["alerta_js"] = utils.criar_alerta_js(
                        "Credenciais inválidas. Tente novamente."
                    )
                    return render(request, "default/login.html", context)
            elif request.session.get("checkbox_login") == "on":
                # Se a requisição não for POST, verifica se existem dados de login armazenados na sessão
                email_saved = request.session.get("email_saved")
                senha_saved = request.session.get("senha_saved")
                if email_saved and senha_saved:
                    status = autenticar_usuario(request, email_saved, senha_saved)
                    if "set_autenticacao" in context:
                        return status
                    if status:
                        return redirect("dashbord")

            return render(request, "default/login.html", context)
        except Exception as e:
            # Se ocorrer algum erro inesperado, registre o erro e retorne False
            utils.erro(f"Erro durante o login: {str(e)}")
            return render(request, "default/login.html", context)
