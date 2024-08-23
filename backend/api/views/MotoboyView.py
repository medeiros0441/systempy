from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from services import MotoboyService
from serializers import MotoboySerializer
from api.permissions import CustomPermission

class MotoboyViewSet(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="motoboy", auth_required=True)]

    @action(detail=False, methods=['get'])
    def listar_motoboys_por_empresa(self, request):
        status_ok, data, message = MotoboyService.listar_motoboys_por_empresa(request)
        if status_ok:
            return Response(data)
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_motoboy(self, request):
        serializer = MotoboySerializer(data=request.data)
        if serializer.is_valid():
            status_ok, data, message = MotoboyService.create_motoboy(serializer.validated_data, request)
            if status_ok:
                return Response(data)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_motoboy(self, request, pk=None):
        status_ok, data, message = MotoboyService.update_motoboy(pk, request.data, request)
        if status_ok:
            return Response(data)
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_motoboy(self, request, pk=None):
        status_ok, data, message = MotoboyService.delete_motoboy(pk, request)
        if status_ok:
            return Response(data)
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def get_motoboy_by_venda(self, request, pk=None):
        status_ok, data, message = MotoboyService.get_motoboy_by_venda(pk)
        if status_ok:
            return Response(data)
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
