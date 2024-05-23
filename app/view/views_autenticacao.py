from django.contrib.auth import authenticate, login
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from app.static import Alerta, UserInfo
import app.view as view
from app import models 
from django.core.exceptions import PermissionDenied


class views_autenticacao:
    def autenticar_usuario(request, email, senha_digitada):
        try:
            # Verifica se o usuário existe
            usuario = models.Usuario.objects.filter(email=email).first()
            if usuario:
                # Verifica se a senha fornecida corresponde ao hash armazenado
                senha_correta = check_password(senha_digitada, usuario.senha)

                if senha_correta:
                    if not usuario.status_acesso:
                        return (
                            False,
                            "Usuário desativado. Entre em contato com o suporte.",
                        )

                    # Atualiza o último login do usuário
                    usuario.ultimo_login = timezone.now()
                    view.views_configuracao.configuracao_set_session(request, usuario.id_usuario)
                    usuario.save()

                    # Armazena os dados do usuário na sessão
                    request.session["id_usuario"] = usuario.id_usuario
                    request.session["id_empresa"] = usuario.empresa.id_empresa
                    request.session["nivel_usuario"] = usuario.nivel_usuario
                    request.session["status_acesso"] = usuario.status_acesso

                    return True, None
                else:
                    return False, "Credenciais inválidas. Tente novamente."
            else:
                return False, "o email não está cadastrado."

        except Exception as e:
            error_message = f"Erro interno durante a autenticação: {str(e)}."
            return view.views_erro.erro(request, error_message)
