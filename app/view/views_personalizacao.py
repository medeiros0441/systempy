from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import Personalizacao
import json
from ..utils import Utils
from django.core.exceptions import ObjectDoesNotExist
from ..static import UserInfo


class views_personalizacao:
    @csrf_exempt
    @Utils.verificar_permissoes(0, True)
    def list_personalizacao(request):
        try:
            id_empresa = UserInfo.get_id_empresa(request)
            id_usuario = UserInfo.get_id_usuario(request)
            personalizacoes = Personalizacao.objects.filter(
                usuario__empresa_id=id_empresa, usuario_id=id_usuario
            )
            personalizacoes_lista = Utils.modelos_para_lista_json(personalizacoes)
            return JsonResponse(
                {"data": personalizacoes_lista, "success": True}, status=200
            )
        except Personalizacao.DoesNotExist:
            return JsonResponse(
                {"error": "Personalizações não encontradas"}, status=404
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @csrf_exempt
    @Utils.verificar_permissoes(0, True)
    def create_personalizacao(request, data=None):
        if request.method != "POST":
            return JsonResponse({"error": "Método não permitido"}, status=405)

        if data is None:
            try:
                data = json.loads(request.body)
                data["id_usuario"] = UserInfo.get_id_usuario(request)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Dados inválidos"}, status=400)


        try:
            personalizacao = Personalizacao.objects.create(
                usuario_id=data["id_usuario"],
                chave=data["chave"],
                valor=data["valor"],
                descricao=data["descricao"],
                descricao_interna=data["descricao_interna"],
                codigo=data["codigo"],
            )
            return JsonResponse(
                {"data": Utils.modelo_para_json(personalizacao), "success": True},
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get_registro_diario_id(usuario_id):
        """
        Obtém o registro diário com base no ID do usuário.
        """
        obj = views_personalizacao.get_personalizacao_codigo(usuario_id, 2)
        return obj.data.valor if obj else None

    def get_loja_id(usuario_id):
        """
        Obtém o id_loja com base no ID do usuário.
        """
        obj = views_personalizacao.get_personalizacao_codigo(usuario_id, 1)
        return obj.data.valor if obj else None

    @Utils.verificar_permissoes(0, True)
    @csrf_exempt
    def get_personalizacao(request, id):

        id_empresa = UserInfo.get_id_empresa(request)
        id_usuario = UserInfo.get_id_usuario(request)
        try:
            personalizacao = Personalizacao.objects.get(
                id_personalizacao=id,
                usuario__empresa_id=id_empresa,
                usuario_id=id_usuario,
            )
            return JsonResponse(
                {"data": Utils.modelo_para_json(personalizacao), "success": True},
                status=201,
            )
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)

    @Utils.verificar_permissoes(0, True)
    @csrf_exempt
    def get_personalizacao_codigo(request, id_usuario, codigo):
        """
        Obtém a personalização com base no ID do usuário e código.
        """
        try:
            personalizacao = Personalizacao.objects.filter(
                codigo=codigo,
                usuario_id=id_usuario,
            ).first()
            if not personalizacao:
                raise ObjectDoesNotExist
            return JsonResponse(
                {"data": Utils.modelo_para_json(personalizacao), "success": True},
                status=201,
            )
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)

    @Utils.verificar_permissoes(0, True)
    @csrf_exempt
    def update_personalizacao(request, id, data=None):
        if request.method != "PUT":
            return JsonResponse({"error": "Método não permitido"}, status=405)

        if data is None:
            try:
                data = json.loads(request.body)
                data["id_empresa"] = UserInfo.get_id_empresa(request)
                data["id_usuario"] = UserInfo.get_id_usuario(request)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Dados inválidos"}, status=400)

        try:
            personalizacao = Personalizacao.objects.get(
                id_personalizacao=id,
                usuario__empresa_id=data["id_empresa"],
                usuario_id=data["id_usuario"],
            )

            personalizacao.chave = data.get("chave", personalizacao.chave)
            personalizacao.valor = data.get("valor", personalizacao.valor)
            personalizacao.descricao = data.get("descricao", personalizacao.descricao)
            personalizacao.descricao_interna = data.get(
                "descricao_interna", personalizacao.descricao_interna
            )
            personalizacao.codigo = data.get("codigo", personalizacao.codigo)

            personalizacao.save()

            return JsonResponse(
                {"data": Utils.modelo_para_json(personalizacao), "success": True},
                status=201,
            )
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @csrf_exempt
    @Utils.verificar_permissoes(0, True)
    def delete_personalizacao(request, id):
        try:
            personalizacao = Personalizacao.objects.get(id_personalizacao=id)
            personalizacao.delete()
            return JsonResponse({"message": "Personalização deletada com sucesso!"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
