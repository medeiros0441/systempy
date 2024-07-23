# middlewares.py

import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

# Configuração do logger para registrar logs de solicitações


class Middleware(MiddlewareMixin):
    # Lista de referers permitidos
    def process_request(self, request):
        referer = request.headers.get("Referer")
        allowed_referers = [
            "http://127.0.0.1:8000",
            "https://comercioprime.azurewebsites.net",
        ]
        return referer in allowed_referers
