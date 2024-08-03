import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.http import JsonResponse
 

class TokenManager:

    def csrf_token_view(request):
         return JsonResponse({'csrfToken': get_token(request)})
    @staticmethod
    def create_token(
        nome_token, payload, time, httponly=False, secure=True, samesite="Strict"
    ):
        # Atualiza o payload com a expiração
        payload.update(
            {
                "exp": datetime.utcnow() + timedelta(hours=time),  # Expiração do token
            }
        )

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = JsonResponse({"message": "Usuário logado."})

        # Define o token no cookie
        response.set_cookie(
            key=nome_token,
            value=token,
            httponly=httponly,  # valor variável
            secure=secure,  # Use True se estiver usando HTTPS
            samesite=samesite,  # Adicione mais segurança ao cookie
        )

        return response

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
