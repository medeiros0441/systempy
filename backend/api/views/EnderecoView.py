from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions import CustomPermission
from api.services import  EnderecoService
from api.models import EnderecoModel
from api.utils import Utils

class EnderecoView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="endereco", auth_required=True)]

    @action(detail=False, methods=['post'])
    def create_endereco(self, request):
        data = request.data
        endereco, status_success, msg = EnderecoService.create_endereco_data(data)
        if status_success:
            response_data = Utils.modelo_para_json(endereco)
            return Response({"success": status_success, "data": response_data, "message": msg}, status=status.HTTP_201_CREATED)
        return Response({"success": status_success, "message": msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_endereco(self, request, pk=None):
        endereco_id = pk
        data = request.data
        endereco, status_success, msg = EnderecoService.update_endereco_data(endereco_id, data)
        if status_success:
            return Response({"success": status_success, "data": Utils.modelo_para_json(endereco), "message": msg}, status=status.HTTP_200_OK)
        return Response({"success": status_success, "message": msg}, status=status.HTTP_404_NOT_FOUND)
