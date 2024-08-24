from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions import CustomPermission
from api.services import  LojaService
from api.utils import Utils
from django.shortcuts import get_object_or_404
from api.models import LojaModel, EmpresaModel, UsuarioModel
from api.user import UserInfo
class LojaView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="loja", auth_required=True)]

    @action(detail=False, methods=['get'])
    def list(self, request):
        id_empresa = UserInfo.get_id_empresa(request)
        lojas_json, success, msg = LojaService.list_lojas(id_empresa)
        if success:
            return Response({"lojas": lojas_json, "success": True}, status=status.HTTP_200_OK)
        return Response({"error": msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def create(self, request):
        data = request.data
        usuario_id = UserInfo.get_id_usuario(request)
        empresa_instance = get_object_or_404(EmpresaModel, id_empresa=UserInfo.get_id_empresa(request, True))
        loja, success, msg = LojaService.create_loja(data, empresa_instance, usuario_id)
        if success:
            response_data = Utils.modelo_para_json(loja)
            return Response({"success": True, "data": response_data, "message": msg}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update(self, request, pk=None):
        loja_id = pk
        data = request.data
        loja, success, msg = LojaService.update_loja(loja_id, data)
        if success:
            response_data = Utils.modelo_para_json(loja)
            return Response({"success": True, "data": response_data, "message": msg}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": msg}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        loja_id = pk
        success, msg = LojaService.delete_loja(loja_id)
        if success:
            return Response({"success": True, "message": msg}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": msg}, status=status.HTTP_404_NOT_FOUND)
