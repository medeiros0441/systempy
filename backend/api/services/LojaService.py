from api.utils import Utils
from api.models import LojaModel, EnderecoModel, AssociadoModel, UsuarioModel, EmpresaModel
from django.shortcuts import get_object_or_404
class LojaService:
    @staticmethod
    def create_loja(data):
        """
        Cria uma nova loja.
        """
        loja = LojaModel(**data)
        loja.save()
        return loja

    @staticmethod
    def get_all_lojas():
        """
        Retorna todas as lojas.
        """
        return LojaModel.objects.all()

    @staticmethod
    def get_loja_by_id(loja_id):
        """
        Retorna uma loja específica pelo ID.
        """
        return get_object_or_404(LojaModel, id_loja=loja_id)

    @staticmethod
    def update_loja(loja_id, data):
        """
        Atualiza uma loja específica.
        """
        loja = get_object_or_404(LojaModel, id_loja=loja_id)
        for attr, value in data.items():
            setattr(loja, attr, value)
        loja.save()
        return loja

    @staticmethod
    def delete_loja(loja_id):
        """
        Deleta uma loja específica.
        """
        loja = get_object_or_404(LojaModel, id_loja=loja_id)
        loja.delete()
        return True

    @staticmethod
    def associate_usuario_loja(id_usuario, id_loja, status_acesso):
        """
        Associa um usuário a uma loja, validando se o usuário existe e se pertence à mesma empresa da loja.
        """
        usuario = get_object_or_404(UsuarioModel, id_usuario=id_usuario)
        loja = get_object_or_404(LojaModel, id_loja=id_loja)

        # Valida se a empresa do usuário é a mesma da loja
        if usuario.empresa_id != loja.empresa_id:
            raise ValueError("O usuário não pertence à mesma empresa que a loja.")

        associado = AssociadoModel(usuario=usuario, loja=loja, status_acesso=status_acesso)
        associado.save()
        return associado