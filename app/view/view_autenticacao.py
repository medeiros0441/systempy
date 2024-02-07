from django.contrib.auth import authenticate, login
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from datetime import timedelta
from ..models.usuario import Usuario
from ..def_global import erro, criar_alerta_js
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password

MAX_TENTATIVAS_INVALIDAS = (
    3  # Número máximo de tentativas de login inválidas permitidas
)
TEMPO_BLOQUEIO = 5  # Tempo de bloqueio em minutos após atingir o número máximo de tentativas inválidas


def autenticar_usuario(request, email, senha_digitada):
    try:
        # Verifica se o usuário existe
        usuario = Usuario.objects.filter(email=email).first()
        if usuario:
            usuario = Usuario.objects.get(email=email)
            # Verifica se o usuário está bloqueado devido a muitas tentativas inválidas
            tentativas_invalidas = request.session.get("tentativas_invalidas", 0)
            tempo_bloqueio_expirado = request.session.get("tempo_bloqueio_expirado")

            if (
                tentativas_invalidas >= MAX_TENTATIVAS_INVALIDAS
                and not tempo_bloqueio_expirado
            ):
                # Usuário bloqueado devido a muitas tentativas inválidas
                raise SuspiciousOperation(
                    f"Usuário bloqueado. Tente novamente após {TEMPO_BLOQUEIO} minutos."
                )
            # Verifica se a senha fornecida corresponde ao hash armazenado
            senha_correta = check_password(senha_digitada, usuario.senha)

            if senha_correta:
                # Atualiza o último login do usuário
                usuario.ultimo_login = timezone.now()
                usuario.save()
                # Armazena os dados do usuário na sessão
                request.session["id_usuario"] = usuario.id_usuario
                request.session["id_empresa"] = usuario.fk_empresa
                request.session["nivel_usuario"] = usuario.nivel_usuario

                # Reseta o contador de tentativas inválidas
                request.session["tentativas_invalidas"] = 0
                request.session["tempo_bloqueio_expirado"] = None
                return redirect("home_cliente")
            else:
                # Aumenta o contador de tentativas inválidas
                request.session.setdefault("tentativas_invalidas", 0)
                request.session["tentativas_invalidas"] += 1
                if request.session["tentativas_invalidas"] >= MAX_TENTATIVAS_INVALIDAS:
                    # Define o tempo de bloqueio
                    request.session["tempo_bloqueio_expirado"] = (
                        timezone.now() + timedelta(minutes=TEMPO_BLOQUEIO)
                    )

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
