from django.core.exceptions import ObjectDoesNotExist
from api.serializers import UsuarioSerializer
from django.shortcuts import get_object_or_404

from api.models import UsuarioModel, LojaModel, AssociadoModel

from django.utils import timezone

from django.contrib.auth.hashers import make_password
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

    @staticmethod
    def create_usuario(data):
        usuario = UsuarioModel.objects.create(**data)
        return usuario
    @staticmethod 
    def get_all_usuarios():
        return UsuarioModel.objects.all()

    @staticmethod
    def get_usuarios_by_empresa(id_empresa):
        """
        Retorna todos os usuários associados a uma empresa específica.
        """
        return UsuarioModel.objects.filter(empresa_id=id_empresa)

    @staticmethod
    def get_usuario_by_id(usuario_id):
        """
        Retorna um único usuário baseado no ID fornecido.
        """
        return UsuarioModel.objects.get(id=usuario_id)

    @staticmethod
    def get_usuarios_by_status(status):
        """
        Retorna todos os usuários com um status específico.
        """
        return UsuarioModel.objects.filter(status_acesso=status)

    @staticmethod
    def get_usuarios_count_by_empresa(id_empresa):
        """
        Retorna a contagem de usuários associados a uma empresa específica.
        """
        return UsuarioModel.objects.filter(empresa_id=id_empresa).count()

    @staticmethod
    def get_usuario_by_id(usuario_id):
        try:
            return UsuarioModel.objects.get(id_usuario=usuario_id)
        except UsuarioModel.DoesNotExist:
            return None

    @staticmethod
    def update_usuario(usuario_id, data):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if usuario:
            for attr, value in data.items():
                setattr(usuario, attr, value)
            usuario.save()
            return usuario
        return None

    @staticmethod
    def delete_usuario(usuario_id):
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if usuario:
            usuario.delete()
            return True
        return False
    
    @staticmethod
    def bloquear_usuario(id_usuario):
        usuario = get_object_or_404(UsuarioModel, id_usuario=id_usuario)
        usuario.status_acesso = False
        usuario.update = timezone.now()
        usuario.save()
        return usuario

    @staticmethod
    def ativar_usuario(id_usuario):
        usuario = get_object_or_404(UsuarioModel, id_usuario=id_usuario)
        usuario.status_acesso = True
        usuario.update = timezone.now()
        usuario.save()
        return usuario
    
    @staticmethod
    def exist_nome_usuario(nome_usuario):
        """
        Verifica se um usuário existe pelo nome de usuário.
        Retorna True se existir, False caso contrário.
        """
        try:
            UsuarioModel.objects.get(nome_usuario=nome_usuario)
            return True
        except ObjectDoesNotExist:
            return False