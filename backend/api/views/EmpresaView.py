# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import EmpresaModel
from api.serializers import EmpresaSerializer
from api.services import  EmpresaService
from api.permissions import CustomPermission

class EmpresaView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="empresa", auth_required=True)]

    def list_private(self, request):
        try:
            empresas = EmpresaService.get_all_empresas()
            serializer = EmpresaSerializer(empresas, many=True)
            return Response({"data": serializer.data, "success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                empresa = EmpresaService.create_empresa(serializer.validated_data)
                return Response({"data": EmpresaSerializer(empresa).data, "success": True}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            empresa = EmpresaService.get_empresa_by_id(pk)
            serializer = EmpresaSerializer(empresa)
            return Response({"data": serializer.data, "success": True}, status=status.HTTP_200_OK)
        except EmpresaModel.DoesNotExist:
            return Response({"error": "Empresa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            empresa = EmpresaService.get_empresa_by_id(pk)
            serializer = EmpresaSerializer(empresa, data=request.data, partial=True)
            if serializer.is_valid():
                updated_empresa = EmpresaService.update_empresa(pk, serializer.validated_data)
                return Response({"data": EmpresaSerializer(updated_empresa).data, "success": True}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except EmpresaModel.DoesNotExist:
            return Response({"error": "Empresa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            EmpresaService.delete_empresa(pk)
            return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
        except EmpresaModel.DoesNotExist:
            return Response({"error": "Empresa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='telefone/(?P<telefone>[\d\+\-\s]+)')
    def telefone_existe(self, request, telefone=None):
        existe = EmpresaService.telefone_existe(telefone)
        return Response({"existe": existe}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='cpf/(?P<cpf>\d{11})')
    def cpf_existe(self, request, cpf=None):
        existe = EmpresaService.cpf_existe(cpf)
        return Response({"existe": existe}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='cnpj/(?P<cnpj>\d{14})')
    def cnpj_existe(self, request, cnpj=None):
        existe = EmpresaService.cnpj_existe(cnpj)
        return Response({"existe": existe}, status=status.HTTP_200_OK)
