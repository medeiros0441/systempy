from django.http import JsonResponse
from django.utils import timezone
from ..models import Motoboy,Configuracao
from ..static import UserInfo,Alerta
from functools import wraps
from ..def_global import erro, criar_alerta_js,verificar_permissoes
from django.views.decorators.csrf import csrf_exempt

class views_motoboy:
    
    @staticmethod
    @csrf_exempt
    @verificar_permissoes(codigo_model=9)
    def listar_motoboys_por_empresa(request):
        if request.method == 'GET':
            id_empresa = UserInfo.get_id_empresa(request, True)
            if id_empresa:
                motoboys = Motoboy.objects.filter(empresa_id=id_empresa)
                motoboy_list = [
                    {'id_motoboy': str(motoboy.id_motoboy), 'nome': motoboy.nome, 'numero': motoboy.numero}
                    for motoboy in motoboys
                ]
                return JsonResponse({'status': 'success', 'motoboys': motoboy_list})
            else:
                return JsonResponse({'status': 'error', 'message': 'ID da empresa não encontrado'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Método não permitido'})
    
    @staticmethod
    @csrf_exempt
    @verificar_permissoes(codigo_model=9)
    def create_motoboy(request):
        if request.method == 'POST':
            data = request.POST
            nome = data.get("nome")
            numero = data.get("numero")
            id_empresa = UserInfo.get_id_empresa(request, True)

            if nome and numero and id_empresa:
                motoboy = Motoboy.objects.create(
                    nome=nome, numero=numero, empresa_id=id_empresa
                )
                return JsonResponse({"status": "success", "id_motoboy": str(motoboy.id_motoboy)})
            else:
                return JsonResponse({"status": "error", "message": "Dados insuficientes para criar o motoboy"})
        else:
            return JsonResponse({"status": "error", "message": "Método não permitido"})
    
    @staticmethod
    @csrf_exempt
    @verificar_permissoes(codigo_model=9)
    def update_motoboy(request, id_motoboy):
        if request.method == 'POST':
            data = request.POST
            nome = data.get("nome")
            numero = data.get("numero")
            id_empresa = UserInfo.get_id_empresa(request, True)

            if nome and numero and id_empresa:
                motoboy = Motoboy.objects.filter(
                    id_motoboy=id_motoboy, empresa_id=id_empresa
                ).first()
                if motoboy:
                    motoboy.nome = nome
                    motoboy.numero = numero
                    motoboy.save()
                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "error", "message": "Motoboy não encontrado"})
            else:
                return JsonResponse({"status": "error", "message": "Dados insuficientes para atualizar o motoboy"})
        else:
            return JsonResponse({"status": "error", "message": "Método não permitido"})
    
    @staticmethod
    @csrf_exempt
    @verificar_permissoes(codigo_model=9)
    def delete_motoboy(request, id_motoboy):
        if request.method == 'DELETE':
            id_empresa = UserInfo.get_id_empresa(request, True)

            if id_empresa:
                motoboy = Motoboy.objects.filter(
                    id_motoboy=id_motoboy, empresa_id=id_empresa
                ).first()
                if motoboy:
                    motoboy.delete()
                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "error", "message": "Motoboy não encontrado"})
            else:
                return JsonResponse({"status": "error", "message": "ID da empresa não encontrado"})
        else:
            return JsonResponse({"status": "error", "message": "Método não permitido"})
