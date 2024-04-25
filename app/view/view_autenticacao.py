from django.contrib.auth import authenticate, login
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from datetime import timedelta
from ..models.usuario import Usuario
from ..def_global import erro, criar_alerta_js
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from ..static import Alerta, UserInfo

MAX_TENTATIVAS_INVALIDAS = (
    3  # Número máximo de tentativas de login inválidas permitidas7
)
TEMPO_BLOQUEIO = 5  # Tempo de bloqueio em minutos após atingir o número máximo de tentativas inválidas


def autenticar_usuario(request, email, senha_digitada):
    try:
        # Verifica se o usuário existe
        usuario = Usuario.objects.filter(email=email).first()
        if usuario:
            usuario = Usuario.objects.get(email=email)

            # Verifica se a senha fornecida corresponde ao hash armazenado
            senha_correta = check_password(senha_digitada, usuario.senha)

            if senha_correta:
                UserInfo.set_id_usuario(request, email, senha_digitada)
                # Atualiza o último login do usuário
                usuario.ultimo_login = timezone.now()
                usuario.save()
                # Armazena os dados do usuário na sessão
                request.session["id_usuario"] = usuario.id_usuario
                request.session["id_empresa"] = usuario.empresa.id_empresa
                request.session["nivel_usuario"] = usuario.nivel_usuario
                request.session["status_acesso"] = usuario.status_acesso

                # Reseta o contador de tentativas inválidas
                request.session["tentativas_invalidas"] = 0
                request.session["tempo_bloqueio_expirado"] = None
                return redirect("dashbord")
            else:

                # Exceção para tentativas inválidas
                script = criar_alerta_js("Credenciais inválidas. Tente novamente.")
                return render(request, "default/login.html", {"alerta_js": script})

        else:
            # Se o usuário não existe, execute a função de erro leve
            return render(
                request,
                "default/login.html",
                {"alerta_js": criar_alerta_js("Email não encontrado.")},
            )

    except Exception as e:
        # Se ocorrer algum erro inesperado, execute a função de erro grave e registre o erro
        return erro(request, f"Erro durante a autenticação: {str(e)}")
