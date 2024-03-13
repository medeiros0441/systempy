from django.shortcuts import render, get_object_or_404, redirect


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


from django.contrib.auth.hashers import check_password
from .models.usuario import Usuario


class UserInfo:
    @staticmethod
    def set_id_usuario(request, email, senha):
        try:
            usuario = Usuario.objects.get(email=email)
            # Verifica se a senha fornecida corresponde ao hash armazenado
            if check_password(senha, usuario.senha):
                request.session["id_usuario"] = usuario.id_usuario
                request.session["id_empresa"] = usuario.empresa.id_empresa
                return True, "Usuário autenticado com sucesso."
            else:
                return False, "Senha inválida"
        except Usuario.DoesNotExist:
            return False, "E-mail inválido"

    @staticmethod
    def get_id_usuario(request):
        return request.session.get("id_usuario")

    @staticmethod
    def get_id_empresa(request, isRequerido=False):
        id_empresa = request.session.get("id_empresa")
        if isRequerido == True and id_empresa is None:
            Alerta.set_mensagem("Vôce precisa Fazer o login.")
            return None
        return id_empresa
    
    @staticmethod
    def is_client(request):
        key = UserInfo.get_id_empresa(request)
        if key > 0:
            return True
        return False
    
    @staticmethod
    def clear_user_info(request):
        if "id_usuario" in request.session:
            del request.session["id_usuario"]
        if "id_empresa" in request.session:
            del request.session["id_empresa"]
