from django.http import JsonResponse
from django.utils import timezone

import jwt
from django.conf import settings
from django.http import HttpResponseForbidden
from datetime import datetime
from django.utils import timezone
from .models import Usuario,Empresa

class Alerta:
    _mensagem = None

    @staticmethod
    def set_mensagem(mensagem):
        Alerta._mensagem = mensagem

    @staticmethod
    def get_mensagem():
        mensagem = Alerta._mensagem
        Alerta._mensagem = None  # Limpa a mensagem após ser lida
        return mensagem


class UserInfo:

    @staticmethod
    def _decode_jwt_token(token):
        try:
            # Decodifica o token usando a chave secreta
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            # Token expirado
            return None
        except jwt.InvalidTokenError:
            # Token inválido
            return None

    @staticmethod
    def get_id_usuario(request):
        token = request.COOKIES.get("jwt_token")
        if token:
            decoded_token = UserInfo._decode_jwt_token(token)
            if decoded_token:
                return decoded_token.get("id_usuario")
        return None

    @staticmethod
    def get_id_empresa(request):
        token = request.COOKIES.get("jwt_token")
        if token:
            decoded_token = UserInfo._decode_jwt_token(token)
            if decoded_token:
                return decoded_token.get("id_empresa")
        return None

    @staticmethod
    def clear_user_info(response):
        response.delete_cookie("jwt_token")
        return response
    
    @staticmethod
    def is_authenticated(request):
        user_id = UserInfo.get_id_usuario(request)
        empresa_id = UserInfo.get_id_empresa(request)
        
        # Verifica se o token contém IDs válidos e se o usuário e empresa existem
        if user_id and empresa_id:
            try:
                usuario = Usuario.objects.get(id_usuario=user_id,empresa_id=empresa_id)
                empresa = Empresa.objects.get(id_empresa=empresa_id)
                return True
            except Usuario.DoesNotExist:
                Alerta.set_mensagem("Usuário não encontrado.")
                return False
            except Empresa.DoesNotExist:
                Alerta.set_mensagem("Empresa não encontrada.")
                return False
        return False