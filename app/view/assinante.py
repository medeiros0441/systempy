from django.shortcuts import render, redirect
from ..def_global import criar_alerta_js, erro
from django.utils import timezone
from .view_cadastro import cadastro_empresa
from .view_autenticacao import autenticar_usuario
from ..gerencia_email.config_email import enviar_email
from ..static import Alerta, UserInfo
from django.http import JsonResponse
from ..def_global import erro, criar_alerta_js, get_status, verificar_permissoes


class views_assinante:

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def dashbord(request):
        return render(request, "assinante/home.html")

    @staticmethod
    @verificar_permissoes(codigo_model=1)
    def desconect(request):
        UserInfo.clear_user_info(request)
        Alerta.set_mensagem("Desconectado.")
        return redirect("home")
