from api.utils import Utils
from api.user import UserInfo
from api.permissions import CustomPermission
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action        
from api.services import ClienteService, EnderecoService
import json
 
 
class ClienteView(viewsets.ViewSet):
    permission_classes = [CustomPermission]  # Permissão base

    def get_permissions(self):
        """
        Ajusta as permissões dinamicamente com base na view.
        """

        permissions = [permission() for permission in self.permission_classes]
        for permission in permissions:
            if isinstance(permission, CustomPermission):
                # Ajuste os parâmetros conforme necessário
                permission.codigo_model = "cliente"
                permission.auth_required = True
        return permissions

    
    def create(self, request):
        try:
            data = json.loads(request.body)
            empresa_id = UserInfo.get_id_empresa(request)

            cliente_data = data.get("cliente", {})
            cliente_data["empresa"] = empresa_id
            
            # Criar o cliente
            cliente, status_cliente, msg_cliente = ClienteService.create_cliente(cliente_data)
            
            if status_cliente:
                response_data = Utils.modelo_para_json(cliente)
                return Response({
                    "success": status_cliente,
                    "data": response_data,
                    "message": msg_cliente
                })
            else:
                return Response({
                    "success": False,
                    "message": msg_cliente
                }, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({
                "error": "Erro ao processar dados JSON."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='atualizar')
    def put(self, request, pk=None):
        """Handle PUT requests to update a cliente by ID."""
        try:
            cliente_data = request.data.get("cliente", {})

            if not cliente_data.get("id_cliente"):
                return Response({"success": False, "message": "ID do cliente não fornecido para atualização."}, status=status.HTTP_400_BAD_REQUEST)

            cliente, status_cliente, msg_cliente = ClienteService.update_cliente(cliente_data["id_cliente"], cliente_data)

            if status_cliente:
                return Response({ "data": Utils.modelo_para_json(cliente), "message": msg_cliente}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": msg_cliente}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='detalhes')
    def get(self, request, pk=None):
        """Handle GET requests to retrieve a cliente by ID."""
        try:
            data = ClienteService.get_cliente(pk)
            if data.get('success'):
                return Response(data, status=status.HTTP_200_OK)
            return Response(data, status=data.get('status', status.HTTP_400_BAD_REQUEST))
        except Exception as e:
            return Response({"message": f"Ocorreu um erro ao processar a solicitação: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'], url_path='excluir')
    def delete_cliente(self, request, pk=None):
        """Handle DELETE requests to delete a cliente by ID."""
        empresa_id = UserInfo.get_id_empresa(request)
        
        # Chama o serviço para excluir o cliente e obtém a resposta
        success, message = ClienteService.delete_cliente(pk, empresa_id)
        
        # Define o status HTTP baseado no sucesso da operação
        if success:
            return Response({ "message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='clientes-empresa')
    def get_clientes_by_empresa(self, request):
        try:
            empresa_id = UserInfo.get_id_empresa(request)
            clientes_data = ClienteService.get_clientes_by_empresa(empresa_id)
            
            # Verifica se há dados retornados e determina o status
            if clientes_data:
                return Response({ "data": clientes_data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Não foram encontrados clientes para esta empresa."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "Erro interno do servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='clientes')
    def get_cliente(self, request):
        empresa_id = UserInfo.get_id_empresa(request)
        response_data, status_code = ClienteService.get_cliente(empresa_id)
        return Response(response_data, status=status_code)

    @action(detail=True, methods=['get'], url_path='vendas')
    def get_vendas_by_cliente(self, request, pk=None):
        response_data, status_code = ClienteService.get_vendas_by_cliente(pk)
        return Response(response_data, status=status_code)