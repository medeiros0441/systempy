from api.utils import Utils
from api.user import UserInfo
from api.permissions import permissions,CustomPermission
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action        
from api.services import ClienteService, EnderecoService
import json
 
 
class ClienteView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="cliente", auth_required=True)]

    @action(methods=['post'], detail=False, url_path='create')
    def create_cliente(self, request):
        try:
            data = json.loads(request.body)
            empresa_id = UserInfo.get_id_empresa(request)

            cliente_data = data.get("cliente", {})
            endereco_data = data.get("endereco", {})
            cliente_data["empresa_id"] = empresa_id

            # Criar o endereço
            endereco, status_endereco, msg_endereco = EnderecoService.create_endereco(endereco_data)
            if not status_endereco:
                return Response({"success": False, "message": msg_endereco}, status=status.HTTP_400_BAD_REQUEST)

            # Criar o cliente
            cliente, status_cliente, msg_cliente = ClienteService.create_cliente(cliente_data, endereco.id_endereco)
            if status_cliente:
                response_data = Utils.modelo_para_json(cliente, endereco)
                return Response({"success": status_cliente, "data": response_data, "message": msg_cliente})
            else:
                return Response({"success": False, "message": msg_cliente}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=False, url_path='update')
    def update_cliente(self, request):
        try:
            data = json.loads(request.body)
            cliente_data = data.get("cliente", {})
            endereco_data = data.get("endereco", {})

            if not endereco_data.get("id_endereco"):
                return Response({"success": False, "message": "Não foi possível recuperar o id_endereco para atualizar."}, status=status.HTTP_400_BAD_REQUEST)

            if not cliente_data.get("id_cliente"):
                return Response({"success": False, "message": "Não foi possível recuperar o id_cliente para atualizar."}, status=status.HTTP_400_BAD_REQUEST)

            # Atualizar o endereço
            endereco, status_endereco, msg_endereco = EnderecoService.update_endereco(endereco_data["id_endereco"], endereco_data)
            if not status_endereco:
                return Response({"success": False, "message": msg_endereco}, status=status.HTTP_400_BAD_REQUEST)

            # Atualizar o cliente
            cliente, status_cliente, msg_cliente = ClienteService.update_cliente(cliente_data["id_cliente"], cliente_data)
            if status_cliente:
                return Response({"success": status_cliente, "data": Utils.modelo_para_json(cliente), "message": msg_cliente})
            else:
                return Response({"success": status_cliente, "message": msg_cliente}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='detalhes')
    def get_cliente(self, request, pk=None):
        """Handle GET requests to retrieve a cliente by ID."""
        data = ClienteService.get_cliente(pk)
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='excluir')
    def delete_cliente(self, request, pk=None):
        """Handle DELETE requests to delete a cliente by ID."""
        empresa_id = UserInfo.get_id_empresa(request)
        response_data, response_status = ClienteService.delete_cliente(pk, empresa_id)
        return Response(response_data, status=response_status)
 
    @action(detail=False, methods=['get'], url_path='clientes-empresa')
    def get_clientes_by_empresa(self, request):
        empresa_id = UserInfo.get_id_empresa(request)
        response_data, status_code = ClienteService.get_clientes_by_empresa(empresa_id)
        return Response(response_data, status=status_code)

    @action(detail=False, methods=['get'], url_path='clientes')
    def get_cliente(self, request):
        empresa_id = UserInfo.get_id_empresa(request)
        response_data, status_code = ClienteService.get_cliente(empresa_id)
        return Response(response_data, status=status_code)

    @action(detail=True, methods=['get'], url_path='vendas')
    def get_vendas_by_cliente(self, request, pk=None):
        response_data, status_code = ClienteService.get_vendas_by_cliente(pk)
        return Response(response_data, status=status_code)