from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from api.permissions import CustomPermission
from rest_framework import viewsets, status

class ErroView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="configuracao", auth_required=True)]

    @staticmethod
    def erro(request, error_message):
        return JsonResponse({"error_message": error_message}, status=500)
