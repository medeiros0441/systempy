from django.http import JsonResponse
from api.models import PersonalizacaoModel, PdvModel, LojaModel
import json
from ..utils import Utils
from django.core.exceptions import ObjectDoesNotExist
from ..user import UserInfo
from uuid import UUID 
from api.permissions import permissions,CustomPermission
from rest_framework import viewsets, status

class PersonalizacaoView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="personalizacao", auth_required=True)]


   
    def list_personalizacao(request):
        try:
            id_empresa = UserInfo.get_id_empresa(request)
            id_usuario = UserInfo.get_id_usuario(request)
            personalizacoes = PersonalizacaoModel.objects.filter(
                usuario__empresa_id=id_empresa, usuario_id=id_usuario
            )
            personalizacoes_lista = Utils.modelos_para_lista_json(personalizacoes)
            return JsonResponse(
                {"data": personalizacoes_lista, "success": True}, status=200
            )
        except PersonalizacaoModel.DoesNotExist:
            return JsonResponse(
                {"error": "Personalizações não encontradas"}, status=404
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

   
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
            personalizacao = PersonalizacaoModel.objects.create(
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

   
    def get_personalizacao_for_venda(request):
        """
        Função para obter a personalização para uma venda.
        """
        try:
            id_usuario = UserInfo.get_id_usuario(request)
            id_loja = PersonalizacaoView.get_loja_id(id_usuario)
            id_pdv = PersonalizacaoView.get_pdv(id_usuario)

            loja = LojaModel.objects.get(id_loja=int(id_loja))
            pdv = PdvModel.objects.get(id_pdv=UUID(id_pdv))

            return JsonResponse(
                {"data": Utils.modelo_para_json(loja, pdv), "success": True},
                status=201,
            )
        except LojaModel.DoesNotExist:
            return JsonResponse({"error": "LojaModel não encontrada."}, status=404)
        except PdvModel.DoesNotExist:
            return JsonResponse({"error": "PdvModel não encontrado."}, status=404)
        except ValueError as ve:
            return JsonResponse({"error": f"Erro de valor: {str(ve)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erro inesperado: {str(e)}"}, status=400)

   
    def get_personalizacao(request, id):

        id_empresa = UserInfo.get_id_empresa(request)
        id_usuario = UserInfo.get_id_usuario(request)
        try:
            personalizacao = PersonalizacaoModel.objects.get(
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

   
    def api_get_personalizacao_codigo(request, id_usuario, codigo):
        """
        Obtém a personalização com base no ID do usuário e código.
        """
        try:
            personalizacao, status, msg = (
                PersonalizacaoView.get_personalizacao_codigo(id_usuario, codigo)
            )
            if not personalizacao:
                return JsonResponse(
                    {"error": "Personalização não encontrada"}, status=404
                )

            return JsonResponse(
                {"data": Utils.modelo_para_json(personalizacao), "success": True},
                status=200,
            )
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)

    def get_personalizacao_codigo(id_usuario, codigo):
        """
        Obtém a personalização com base no ID do usuário e código.
        """
        personalizacao = PersonalizacaoModel.objects.filter(
            codigo=codigo,
            usuario_id=id_usuario,
        ).first()

        if not personalizacao:
            return None, False, "Não encontrado."

        return personalizacao, True, "Objeto encontrado."

    def get_registro_diario_id(usuario_id):
        """
        Obtém o registro diário com base no ID do usuário.
        """
        personalizacao, status, msg = PersonalizacaoView.get_personalizacao_codigo(
            usuario_id, 2
        )
        return personalizacao.get("valor") if personalizacao else None

    def get_pdv(usuario_id):
        """
        Obtém o registro diário com base no ID do usuário.
        """
        personalizacao, status, msg = PersonalizacaoView.get_personalizacao_codigo(
            usuario_id, 2
        )
        return personalizacao.valor if personalizacao else None

    def get_loja_id(usuario_id):
        """
        Obtém o id_loja com base no ID do usuário.
        """
        personalizacao, status, msg = PersonalizacaoView.get_personalizacao_codigo(
            usuario_id, 1
        )
        return personalizacao.valor if personalizacao else None

   
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
            personalizacao = PersonalizacaoModel.objects.get(
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

   
    def delete_personalizacao(request, id):
        try:
            personalizacao = PersonalizacaoModel.objects.get(id_personalizacao=id)
            personalizacao.delete()
            return JsonResponse({"message": "Personalização deletada com sucesso!"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Personalização não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
