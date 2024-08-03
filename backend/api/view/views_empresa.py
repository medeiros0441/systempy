# views.py
from ..models.empresa import Empresa
import json
from django.http import JsonResponse
from api.utils import Utils
from api.user import UserInfo
from api.permissions import permissions,CustomPermission
from rest_framework.views import APIView
class views_empresa(APIView):
    permission_classes = [CustomPermission(codigo_model="empresa", auth_required=True)]


    @permissions.isAutorizado(0, True)
    def list_empresas(request):
        try:
            empresas = Empresa.objects.all()
            empresas_lista = Utils.modelos_para_lista_json(empresas)
            return JsonResponse({"data": empresas_lista, "success": True}, status=200)
        except Empresa.DoesNotExist:
            return JsonResponse({"error": "Empresas não encontradas"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @permissions.isAutorizado(0, True)
    def create_empresa(request):
        if request.method == "POST":
            data = json.loads(request.body)
            try:
                empresa = Empresa.objects.create(
                    nome_empresa=data["nome_empresa"],
                    nro_cnpj=data["nro_cnpj"],
                    razao_social=data.get("razao_social"),
                    descricao=data.get("descricao"),
                    nome_responsavel=data["nome_responsavel"],
                    cargo=data["cargo"],
                    email=data["email"],
                    nro_cpf=data["nro_cpf"],
                    telefone=data["telefone"],
                )
                return JsonResponse(
                    {"data": Utils.modelo_para_json(empresa), "success": True},
                    status=201,
                )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "Método não permitido"}, status=405)

    @permissions.isAutorizado(0, True)
    def get_empresa(request, id=None):
        try:
            if id is None:
                id = UserInfo.get_id_empresa(request)

            empresa = Empresa.objects.get(pk=id)
            empresa_json = Utils.modelo_para_json(empresa)
            return JsonResponse({"data": empresa_json, "success": True}, status=200)
        except Empresa.DoesNotExist:
            return JsonResponse({"error": "Empresa não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @permissions.isAutorizado(0, True)
    def update_empresa(request, id):
        if request.method == "PUT":
            data = json.loads(request.body)
            try:
                empresa = Empresa.objects.get(pk=id)
                empresa.nome_empresa = data.get("nome_empresa", empresa.nome_empresa)
                empresa.nro_cnpj = data.get("nro_cnpj", empresa.nro_cnpj)
                empresa.razao_social = data.get("razao_social", empresa.razao_social)
                empresa.descricao = data.get("descricao", empresa.descricao)
                empresa.nome_responsavel = data.get(
                    "nome_responsavel", empresa.nome_responsavel
                )
                empresa.cargo = data.get("cargo", empresa.cargo)
                empresa.email = data.get("email", empresa.email)
                empresa.nro_cpf = data.get("nro_cpf", empresa.nro_cpf)
                empresa.telefone = data.get("telefone", empresa.telefone)
                empresa.update = Utils.obter_data_hora_atual()
                empresa.save()
                return JsonResponse(
                    {"data": Utils.modelo_para_json(empresa), "success": True},
                    status=200,
                )
            except Empresa.DoesNotExist:
                return JsonResponse({"error": "Empresa não encontrada"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "Método não permitido"}, status=405)

    @permissions.isAutorizado(0, True)
    def delete_empresa(request, id):
        if request.method == "DELETE":
            try:
                empresa = Empresa.objects.get(pk=id)
                empresa.delete()
                return JsonResponse({"success": True}, status=204)
            except Empresa.DoesNotExist:
                return JsonResponse({"error": "Empresa não encontrada"}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Método não permitido"}, status=405)

    def telefone_existe(telefone):
        from api.models import Empresa
        from api.models import Configuracao

        return Empresa.objects.filter(telefone__iexact=telefone).exists()

    def cpf_existe(cpf):
        from api.models import Empresa

        Empresa.objects.filter(nro_cpf__iexact=cpf).exists()
        return

    def cnpj_existe(cnpj):
        from api.models import Empresa

        return Empresa.objects.filter(nro_cnpj__iexact=cnpj).exists()
