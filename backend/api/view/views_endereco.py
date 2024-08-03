from ..models import Endereco, Configuracao
from api.utils import Utils
from api.user import UserInfo
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from api.permissions import permissions

from api.permissions import permissions,CustomPermission
from rest_framework.views import APIView


class views_endereco(APIView):
    permission_classes = [CustomPermission(codigo_model="endereco", auth_required=True)]


    def api_create_endereco(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                endereco, status, msg = views_endereco.create_endereco_data(data)
                if status:
                    response_data = Utils.modelo_para_json(endereco)
                    return JsonResponse(
                        {"success": status, "data": response_data, "message": msg}
                    )
                else:
                    return JsonResponse({"success": status, "message": msg}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Método não permitido"}, status=405)

    @staticmethod
    @permissions.isAutorizado(8, True)
    def api_update_endereco(request, endereco_id):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                endereco, status, msg = views_endereco.update_endereco_data(
                    endereco_id, data
                )
                if status:
                    return JsonResponse(
                        {
                            "success": status,
                            "data": Utils.modelo_para_json(endereco),
                            "message": msg,
                        }
                    )
                else:
                    return JsonResponse({"success": status, "message": msg}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Método não permitido"}, status=405)

    def create_endereco_data(data):
        """
        Cria uma instância do modelo Endereco com base nos dados fornecidos.
        """
        try:
            endereco = Endereco.objects.create(
                rua=data.get("rua", ""),
                numero=data.get("numero", ""),
                bairro=data.get("bairro", ""),
                cidade=data.get("cidade", ""),
                estado=data.get("estado", ""),
                codigo_postal=data.get("codigo_postal", ""),
                descricao=data.get("descricao", ""),
                insert=Utils.obter_data_hora_atual(),
                update=Utils.obter_data_hora_atual(),
            )
            return endereco, True, "Cadastro de endereço efetuado com sucesso."
        except Exception as e:
            return None, False, f"Erro ao cadastrar endereço: {str(e)}"

    def update_endereco_data(endereco_id, data):
        """
        Atualiza uma instância existente do modelo Endereco com base nos dados fornecidos.
        """
        try:
            endereco = Endereco.objects.get(id_endereco=endereco_id)
            endereco.rua = data.get("rua", endereco.rua)
            endereco.numero = data.get("numero", endereco.numero)
            endereco.bairro = data.get("bairro", endereco.bairro)
            endereco.cidade = data.get("cidade", endereco.cidade)
            endereco.estado = data.get("estado", endereco.estado)
            endereco.codigo_postal = data.get("codigo_postal", endereco.codigo_postal)
            endereco.descricao = data.get("descricao", endereco.descricao)
            endereco.update = Utils.obter_data_hora_atual()
            endereco.save()
            return endereco, True, "Atualização de endereço efetuada."
        except Endereco.DoesNotExist:
            return None, False, f"Endereço com ID {endereco_id} não encontrado."
        except Exception as e:
            return None, False, f"Erro ao atualizar endereço: {str(e)}"
