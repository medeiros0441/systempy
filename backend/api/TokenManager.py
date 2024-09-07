import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.response import Response
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie 
class TokenManager:
    
    
    @ensure_csrf_cookie
    def csrf_token_view(request):
        return Response({'csrfToken': request.COOKIES.get('csrftoken')})
    
    @staticmethod
    def create_token(payload, time):
        # Atualiza o payload com a expiração
        payload.update(
            {
                "exp": datetime.utcnow() + timedelta(hours=time),  # Expiração do token
            }
        )
        # Gera o token JWT
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        # Retorna apenas o token como string
        return token

    @staticmethod
    def read_token(token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def update_token(
        nome_token, payload, time, httponly=False, secure=True, samesite="Strict"
    ):
        return TokenManager.create_token(
            nome_token, payload, time, httponly, secure, samesite
        )

    @staticmethod
    def delete_token(response, name):
        response.delete_cookie(name)
        return response
