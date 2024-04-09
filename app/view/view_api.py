from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Endereco
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..def_global import erro, criar_alerta_js, get_status, verificar_permissoes
from ..models.usuario import Usuario
from ..models import Cliente, Configuracao, Usuario
from ..static import Alerta, UserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class views_api:

    @csrf_exempt
    @staticmethod
    @verificar_permissoes(codigo_model=3)
    def create_endereco(request):
        if request.method == 'POST':
            data = request.POST
            try:
                endereco = Endereco.objects.create(
                    rua=data.get('rua'),
                    numero=data.get('numero'),
                    bairro=data.get('bairro'),
                    cidade=data.get('cidade'),
                    estado=data.get('estado'),
                    codigo_postal=data.get('codigo_postal'),
                    descricao=data.get('descricao')
                )
                return JsonResponse({'message': 'Endereco created successfully'},endereco, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)


    @csrf_exempt
    @staticmethod
    @verificar_permissoes(codigo_model=3)
    def read_endereco(request, endereco_id):
        try:
            endereco = Endereco.objects.get(id=endereco_id)
            data = {
                'id': endereco.id,
                'rua': endereco.rua,
                'numero': endereco.numero,
                'bairro': endereco.bairro,
                'cidade': endereco.cidade,
                'estado': endereco.estado,
                'codigo_postal': endereco.codigo_postal,
                'descricao': endereco.descricao
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Endereco not found'}, status=404)

    @csrf_exempt
    @staticmethod
    @verificar_permissoes(codigo_model=3)
    def update_endereco(request, endereco_id):
        if request.method == 'PUT':
            data = request.POST
            try:
                endereco = Endereco.objects.get(id=endereco_id)
                endereco.rua = data.get('rua', endereco.rua)
                endereco.numero = data.get('numero', endereco.numero)
                endereco.bairro = data.get('bairro', endereco.bairro)
                endereco.cidade = data.get('cidade', endereco.cidade)
                endereco.estado = data.get('estado', endereco.estado)
                endereco.codigo_postal = data.get('codigo_postal', endereco.codigo_postal)
                endereco.descricao = data.get('descricao', endereco.descricao)
                endereco.save()
                return JsonResponse({'message': 'Endereco updated successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

    @csrf_exempt
    @staticmethod
    @verificar_permissoes(codigo_model=3)
    def delete_endereco(request, endereco_id):
        if request.method == 'DELETE':
            try:
                endereco = Endereco.objects.get(id=endereco_id)
                endereco.delete()
                return JsonResponse({'message': 'Endereco deleted successfully'})
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Endereco not found'}, status=404)
