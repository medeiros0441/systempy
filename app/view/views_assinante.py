from django.shortcuts import render, redirect
from django.utils import timezone
from ..gerencia_email.config_email import enviar_email
from django.http import JsonResponse

from app.utils import Utils

from app.static import Alerta, UserInfo


class views_assinante:

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=1)
    def dashbord(request):
        return render(request, "assinante/home.html")

    @staticmethod
    @Utils.verificar_permissoes(codigo_model=1)
    def desconect(request):
        UserInfo.clear_user_info(request)
        Alerta.set_mensagem("Desconectado.")
        return redirect("home")
