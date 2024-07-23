import jwt
from django.conf import settings
from .models import Usuario, Empresa


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
        token = request.COOKIES.get("token_user")
        if token:
            decoded_token = UserInfo._decode_jwt_token(token)
            if decoded_token:
                return decoded_token.get("id_usuario")
        return None

    @staticmethod
    def get_id_empresa(request):
        token = request.COOKIES.get("token_user")
        if token:
            decoded_token = UserInfo._decode_jwt_token(token)
            if decoded_token:
                return decoded_token.get("id_empresa")
        return None

    @staticmethod
    def clear_user_info(response):
        response.delete_cookie("token_user")
        return response

    @staticmethod
    def is_authenticated(request):
        user_id = UserInfo.get_id_usuario(request)
        empresa_id = UserInfo.get_id_empresa(request)

        # Verifica se o token contém IDs válidos e se o usuário e empresa existem
        if user_id and empresa_id:
            try:
                usuario = Usuario.objects.get(id_usuario=user_id, empresa_id=empresa_id)
                empresa = Empresa.objects.get(id_empresa=empresa_id)
                return True, "Usuário autenticado."
            except Usuario.DoesNotExist:
                return False, "Usuário não encontrado."
            except Empresa.DoesNotExist:
                return False, "Empresa não encontrada."
        return False, "Não autenticado."
