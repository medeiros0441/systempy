from django.shortcuts import render, redirect
from django.utils import timezone
from ..gerencia_email.config_email import enviar_email
from django.http import JsonResponse

from api.utils import Utils

from api.static import Alerta, UserInfo


class views_assinante:

    @staticmethod
    @Utils.verificar_permissoes(1, True)
    def dashboard(request):
        return render(request, "assinante/home.html")

    @staticmethod
    @Utils.verificar_permissoes(1, True)
    def desconect(request):
        UserInfo.clear_user_info(request)
        Alerta.set_mensagem("Desconectado.")
        return redirect("home")

    @staticmethod
    @Utils.verificar_permissoes()
    def configuracao(request):
        return render(request, "assinante/configuracao.html")
