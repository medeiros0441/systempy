from django.shortcuts import render, redirect
from ..def_global import criar_alerta_js, erro
from django.utils import timezone
from .view_cadastro import cadastro_empresa
from .view_autenticacao import autenticar_usuario
from ..processador.config_email import enviar_email

def home(request):
    return render(request, "default/home.html")


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
                assunto="Contato via site WMS",
                NomeCliente=nome,
                TextIntroducao=mensagem_modelo,
                TextContainer2=mensagem,
            )

            return render(
                request,
                "default/sobre.html",
                {"alerta_js": criar_alerta_js("Mensagem Enviada.")},
            )
        except Exception as e:
            mensagem_erro = str(e)
        return erro(request, mensagem_erro)
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
        return erro(request, mensagem_erro)


from django.contrib import messages


def login(request):
    try:
        # Obtém o estado do checkbox a partir da sessão
        checkbox_login = request.session.get("checkbox_login", "off")

        if request.method == "POST":
            # Se a requisição for POST, tenta obter os dados de email, senha e checkbox
            email = request.POST.get("email")
            senha = request.POST.get("senha")
            valor_checkbox = request.POST.get("flexCheckDefault")

            if valor_checkbox == "on":
                # Se o checkbox estiver marcado, atualiza o estado da sessão
                request.session["checkbox_login"] = "on"
            else:
                # Se o checkbox não estiver marcado, limpa os dados da sessão relacionados ao login
                request.session.pop("email", None)
                request.session.pop("senha", None)
                request.session.pop("checkbox_login", None)

            # Chama a função para autenticar o usuário com os dados fornecidos
            return autenticar_usuario(request, email, senha)
        else:
            # Se a requisição não for POST, verifica se existem dados de login armazenados na sessão
            if "email" in request.session and "senha" in request.session:
                # Preenche os campos do formulário com os dados armazenados na sessão
                email_saved = request.session["email"]
                senha_saved = request.session["senha"]

                if checkbox_login == "on":
                    # Se o checkbox estava marcado na última sessão, mantém marcado
                    request.session["checkbox_login"] = "on"
                else:
                    # Se o checkbox não estava marcado na última sessão, mantém desmarcado
                    request.session["checkbox_login"] = "off"

                # Renderiza o template com os dados do formulário
                return render(
                    request,
                    "default/login.html",
                    {
                        "checkbox_login": checkbox_login,
                        "email_saved": email_saved,
                        "senha_saved": senha_saved,
                    },
                )
            else:
                # Se não houver dados de login na sessão, renderiza o template sem preenchimento
                return render(
                    request,
                    "default/login.html",
                    {
                        "checkbox_login": checkbox_login,
                    },
                )
    except Exception as e:
        # Trata exceções
        mensagem_erro = str(e)
        print("Erro:", mensagem_erro)
        return erro(request, mensagem_erro)
