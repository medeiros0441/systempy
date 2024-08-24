from api.utils import Utils
from django.http import HttpResponse
from api.models import GalaoModel, ConfiguracaoModel
from .ErroView import ErroView
from api.permissions import permissions, CustomPermission
from rest_framework import viewsets, status
from rest_framework import viewsets, status

class GalaoView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="galao", auth_required=True)]

    @staticmethod
  
    def lista_galao(request):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para listar os galões
            return HttpResponse("Lista de galões")
        else:
            return ErroView.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

  
    def editar_galao(request, galao_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para editar o galão com id=galao_id
            return HttpResponse(f"Editando o galão {galao_id}")
        else:
            return ErroView.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

  
    def selecionar_galao(request, galao_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para selecionar o galão com id=galao_id
            return HttpResponse(f"Selecionando o galão {galao_id}")
        else:
            return ErroView.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

  
    def excluir_galao(request, galao_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para excluir o galão com id=galao_id
            return HttpResponse(f"Excluindo o galão {galao_id}")
        else:
            return ErroView.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )
