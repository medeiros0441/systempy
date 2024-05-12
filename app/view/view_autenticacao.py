from django.contrib.auth import authenticate, login
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from datetime import timedelta
from ..models.usuario import Usuario
from ..utils import utils
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from ..static import Alerta, UserInfo
import traceback


def autenticar_usuario(request, email, senha_digitada):
    try:
        # Verifica se o usuário existe
        usuario = Usuario.objects.filter(email=email).first()
        if usuario:
            # Verifica se a senha fornecida corresponde ao hash armazenado
            senha_correta = check_password(senha_digitada, usuario.senha)

            if senha_correta:
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
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        traceback_info = traceback.format_exc()
            # Constrói a mensagem de erro com a página e a linha específica
        error_message = f"Erro durante a autenticação: {str(e)}. Página: {request.path}. Linha: {traceback_info.splitlines()[-2]}"
            # Se ocorrer algum erro inesperado, execute a função de erro grave e registre o erro
        return utils.erro(request,error_message)
