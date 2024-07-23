from functools import wraps
from .utils import Utils
from .user import UserInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class permissions:

    def isAutorizado(codigo_model=None, auth_required=False):
        """
        Decorador para verifiar as permissões do usuário antes de executar a função.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):

                # Verifica se autenticação é necessária e se o usuário está autenticado
                status, mensage = UserInfo.is_authenticated
                if not status:
                    return False, mensage
                # Configurações de modelo, se aplicável
                id_usuario = UserInfo.get_id_usuario(request)
                if codigo_model:
                    codigo_model_convertido = codigo_model
                    if isinstance(codigo_model, str):
                        lista = Utils.lista_de_configuracao()
                        codigo_model_lower = codigo_model.lower()
                        for item in lista:
                            if item["nome"].lower() == codigo_model_lower:
                                codigo_model_convertido = item["codigo"]
                                break

                    status, render = Utils.configuracao_usuario(
                        request, id_usuario, codigo_model_convertido
                    )
                else:
                    status = True

                if status:
                    return func(request, *args, **kwargs)
                else:
                    return render

            return wrapper

        return decorator
