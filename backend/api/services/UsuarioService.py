from api.models import UsuarioModel
from django.core.exceptions import ObjectDoesNotExist
from api.serializers import UsuarioSerializer


class UsuarioService:

    @staticmethod
    def verificar_email(email, retornar_dados=False):
        """
        Verifica se o e-mail existe no banco de dados.

        :param email: Email a ser verificado.
        :param retornar_dados: Se True, retorna os dados do usuário. Caso contrário, retorna um booleano.
        :return: Booleano se retornar_dados for False, ou dados serializados se retornar_dados for True.
        """
        try:
            usuario = UsuarioModel.objects.get(email=email)
            if retornar_dados:
                serializer = UsuarioSerializer(usuario)
                return serializer.data   
            return True
        except UsuarioModel.DoesNotExist:
            return False if not retornar_dados else None
