from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Personalizacao
import json
from ..utils import Utils
from django.core.exceptions import ObjectDoesNotExist
from ..static import UserInfo


class views_personalizacao:

    @csrf_exempt
    def create_personalizacao(request):
        if request.method == "POST":
            data = json.loads(request.body)
            id_usuario = UserInfo.get_id_usuario(request)
            try:
                personalizacao = Personalizacao.objects.create(
                    usuario_id=id_usuario,
                    chave=data["chave"],
                    valor=data["valor"],
                    descricao=data["descricao"],
                    descricao_interna=data["descricao_interna"],
                    codigo=data["codigo"],
                )
                return JsonResponse(
                    json.loads(Utils.modelo_para_json(personalizacao)), status=201
                )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "Método não permitido"}, status=405)

    def get_personalizacao(request, id):
        id_empresa = UserInfo.get_empresa(request)
        id_usuario = UserInfo.get_id_usuario(request)
        try:
            personalizacao = Personalizacao.objects.get(
                id=id, usuario__empresa_id=id_empresa, usuario_id=id_usuario
            )
            return JsonResponse(json.loads(Utils.modelo_para_json(personalizacao)))
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)

    @csrf_exempt
    def update_personalizacao(request, id):
        if request.method == "PUT":
            data = json.loads(request.body)
            id_empresa = UserInfo.get_empresa(request)
            id_usuario = UserInfo.get_id_usuario(request)
            try:
                personalizacao = Personalizacao.objects.get(
                    id=id, usuario__empresa_id=id_empresa, usuario_id=id_usuario
                )
                personalizacao.chave = data.get("chave", personalizacao.chave)
                personalizacao.valor = data.get("valor", personalizacao.valor)
                personalizacao.descricao = data.get(
                    "descricao", personalizacao.descricao
                )
                personalizacao.descricao_interna = data.get(
                    "descricao_interna", personalizacao.descricao_interna
                )
                personalizacao.codigo = data.get("codigo", personalizacao.codigo)
                personalizacao.save()
                return JsonResponse(json.loads(Utils.modelo_para_json(personalizacao)))
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"error": "Personalização não encontrada"}, status=404
                )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "Método não permitido"}, status=405)

    @csrf_exempt
    def delete_personalizacao(request, id):
        if request.method == "DELETE":
            id_empresa = UserInfo.get_empresa(request)
            id_usuario = UserInfo.get_id_usuario(request)
            try:
                personalizacao = Personalizacao.objects.get(
                    id=id, usuario__empresa_id=id_empresa, usuario_id=id_usuario
                )
                personalizacao.delete()
                return JsonResponse({"message": "Personalização deletada com sucesso!"})
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"error": "Personalização não encontrada"}, status=404
                )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "Método não permitido"}, status=405)

    def list_personalizacao(request):
        id_empresa = UserInfo.get_empresa(request)
        id_usuario = UserInfo.get_id_usuario(request)
        personalizacoes = Personalizacao.objects.filter(
            usuario__empresa_id=id_empresa, usuario_id=id_usuario
        )
        return JsonResponse(
            json.loads(Utils.modelos_para_lista_json(personalizacoes)), safe=False
        )
