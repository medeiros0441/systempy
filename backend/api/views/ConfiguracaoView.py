from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from services import ConfiguracaoService
from models import ConfiguracaoModel
from serializers import ConfiguracaoSerializer
from user import UserInfo
from api.permissions import permissions,CustomPermission

class ConfiguracaoView(viewsets.ViewSet):
    permission_classes = CustomPermission(codigo_model="configuracao", auth_required=True)

    @action(detail=False, methods=['get'], url_path='usuario/(?P<id_usuario>\d+)/')
    def get_configuracoes_usuario(self, request, id_usuario=None):
        response_data, status_code = ConfiguracaoService.get_configuracoes_usuario(id_usuario)
        return Response(response_data, status=status_code)

    @action(detail=False, methods=['post'], url_path='session/(?P<id_usuario>\d+)/')
    def configuracao_set_session(self, request, id_usuario=None):
        response_data, status_code = ConfiguracaoService.configuracao_set_session(request, id_usuario)
        return Response(response_data, status=status_code)

    @action(detail=False, methods=['post'], url_path='criar-padrao/')
    def criar_configuracoes_padrao(self, request):
        listModel = request.data.get('listModel', [])
        response_data, status_code = ConfiguracaoService.criar_configuracoes_padrao(listModel)
        return Response(response_data, status=status_code)

    @action(detail=False, methods=['get'], url_path='listar-padrao/')
    def list_configuracoes_padrao(self, request):
        usuario = UserInfo.get_id_usuario(request)
        response_data = ConfiguracaoService.list_configuracoes_padrao(usuario)
        return Response({"data": response_data, "success": True}, status=status.HTTP_200_OK)
