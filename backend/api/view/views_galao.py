from api.utils import Utils
from django.http import HttpResponse
from ..models import Galao, Configuracao

from .views_erro import views_erro

from api.permissions import permissions


class views_galao:

    @staticmethod
    @permissions.isAutorizado(3, True)
    def lista_galao(request):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para listar os galões
            return HttpResponse("Lista de galões")
        else:
            return views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    @permissions.isAutorizado(3, True)
    def editar_galao(request, galao_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para editar o galão com id=galao_id
            return HttpResponse(f"Editando o galão {galao_id}")
        else:
            return views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    @permissions.isAutorizado(3, True)
    def selecionar_galao(request, galao_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para selecionar o galão com id=galao_id
            return HttpResponse(f"Selecionando o galão {galao_id}")
        else:
            return views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    @permissions.isAutorizado(3, True)
    def excluir_galao(request, galao_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para excluir o galão com id=galao_id
            return HttpResponse(f"Excluindo o galão {galao_id}")
        else:
            return views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )
