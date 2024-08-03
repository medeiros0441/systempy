from django.shortcuts import render, get_object_or_404, redirect
from api.utils import Utils
from api.user import UserInfo
from ..models import Empresa, Loja, Associado, Usuario, Endereco
from .views_erro import views_erro
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from api.permissions import permissions
from django.views.decorators.csrf import csrf_exempt


from api.permissions import permissions,CustomPermission
from rest_framework.views import APIView
class views_loja(APIView):
    permission_classes = [CustomPermission(codigo_model="loja", auth_required=True)]


    @permissions.isAutorizado(5, True)
    def lista_lojas(request):
        try:
            id_empresa = UserInfo.get_id_empresa(request)
            lojas = Loja.objects.filter(empresa_id=id_empresa)
            lojas_json = []
            for loja in lojas:
                loja_data = {
                    "id_loja": loja.id_loja,
                    "nome": loja.nome,
                    "numero_telefone": loja.numero_telefone,
                    "horario_operacao_inicio": (
                        loja.horario_operacao_inicio.strftime("%H:%M:%S")
                        if loja.horario_operacao_inicio
                        else None
                    ),
                    "horario_operacao_fim": (
                        loja.horario_operacao_fim.strftime("%H:%M:%S")
                        if loja.horario_operacao_fim
                        else None
                    ),
                    "segunda": loja.segunda,
                    "terca": loja.terca,
                    "quarta": loja.quarta,
                    "quinta": loja.quinta,
                    "sexta": loja.sexta,
                    "sabado": loja.sabado,
                    "domingo": loja.domingo,
                    "insert": loja.insert,
                    "update": loja.update,
                    "empresa": loja.empresa.id_empresa,
                    "endereco": loja.endereco.id if loja.endereco else None,
                }
                associados = Associado.objects.filter(loja=loja)
                loja_data["associados"] = [
                    {
                        "id_associado": associado.id_associado,
                        "insert": associado.insert,
                        "update": associado.update,
                        "status_acesso": associado.status_acesso,
                        "usuario": {
                            "id_usuario": associado.usuario.id_usuario,
                            "nome_completo": associado.usuario.nome_completo,
                        },
                        "loja": associado.loja.id_loja,
                    }
                    for associado in associados
                ]
                lojas_json.append(loja_data)

            return JsonResponse({"lojas": lojas_json, "success": True})
        except Loja.DoesNotExist:
            return JsonResponse({"lojas": [], "success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @permissions.isAutorizado(5, True)
    def criar_loja(request):
        try:
            data = json.loads(request.body)

            # Validação básica dos dados recebidos
            required_loja_fields = [
                "nome",
                "descricao",
            ]  # Adicione outros campos obrigatórios da Loja aqui
            required_endereco_fields = [
                "rua",
                "cidade",
                "estado",
                "cep",
            ]  # Adicione outros campos obrigatórios do Endereco aqui

            missing_fields = []

            for field in required_loja_fields:
                if field not in data:
                    missing_fields.append(f"loja.{field}")

            for field in required_endereco_fields:
                if field not in data:
                    missing_fields.append(f"endereco.{field}")

            if missing_fields:
                return JsonResponse(
                    {
                        "detail": "Campos obrigatórios ausentes",
                        "missing_fields": missing_fields,
                    },
                    status=400,
                )

            # Obter a instância da Empresa
            id_empresa_get = UserInfo.get_id_empresa(request, True)
            empresa_instance = get_object_or_404(Empresa, id_empresa=id_empresa_get)

            # Criar endereço
            endereco = Endereco(
                rua=data["rua"],
                cidade=data["cidade"],
                estado=data["estado"],
                cep=data["cep"],
            )
            endereco.save()

            # Criar loja
            loja = Loja(
                nome=data["nome"],
                descricao=data["descricao"],
                endereco=endereco,
                empresa=empresa_instance,
            )
            loja.save()

            # Associar usuários
            id_usuario = UserInfo.get_id_usuario(request)
            usuario_adm = Usuario.objects.get(
                empresa_id=loja.empresa_id, nivel_usuario=1
            )

            associados = [
                Associado(usuario_id=id_usuario, loja=loja, status_acesso=True)
            ]

            if usuario_adm.id_usuario != id_usuario:
                associados.append(
                    Associado(usuario=usuario_adm, loja=loja, status_acesso=True)
                )

            Associado.objects.bulk_create(associados)

            return JsonResponse(
                {"detail": f"Loja {loja.nome} criada com sucesso"}, status=201
            )
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse(
                {"detail": "Erro ao processar a solicitação", "error": mensagem_erro},
                status=500,
            )

    @permissions.isAutorizado(5, True)
    def selecionar_loja(request, id_loja):

        try:
            loja = get_object_or_404(Loja, pk=id_loja)
            id = UserInfo.get_id_empresa(request)
            if loja.empresa.id_empresa == id:
                return views_loja.lista_lojas(
                    request,
                    {
                        "open_modal": True,
                        "text_endereco": loja.endereco,
                        "text_loja": loja,
                    },
                )
            else:
                return views_erro.erro(request, "vôce não está associado a empresa..")
        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)

    @permissions.isAutorizado(5, True)
    def editar_loja(request, id_loja):
        try:
            loja = get_object_or_404(Loja, pk=id_loja)
            id_empresa = UserInfo.get_id_empresa(request)

            if loja.empresa.id_empresa != id_empresa:
                return JsonResponse(
                    {"detail": "Você não está associado a esta empresa."}, status=403
                )

            if request.method == "POST":
                data = json.loads(request.body)

                # Validação básica dos dados recebidos
                required_loja_fields = [
                    "nome",
                    "descricao",
                ]  # Adicione outros campos obrigatórios da Loja aqui
                required_endereco_fields = [
                    "rua",
                    "cidade",
                    "estado",
                    "cep",
                ]  # Adicione outros campos obrigatórios do Endereco aqui

                missing_fields = []

                for field in required_loja_fields:
                    if field not in data:
                        missing_fields.append(f"loja.{field}")

                for field in required_endereco_fields:
                    if field not in data:
                        missing_fields.append(f"endereco.{field}")

                if missing_fields:
                    return JsonResponse(
                        {
                            "detail": "Campos obrigatórios ausentes",
                            "missing_fields": missing_fields,
                        },
                        status=400,
                    )

                # Atualizar endereço
                endereco = loja.endereco
                endereco.rua = data.get("rua", endereco.rua)
                endereco.cidade = data.get("cidade", endereco.cidade)
                endereco.estado = data.get("estado", endereco.estado)
                endereco.cep = data.get("cep", endereco.cep)
                endereco.save()

                # Atualizar loja
                loja.nome = data.get("nome", loja.nome)
                loja.descricao = data.get("descricao", loja.descricao)
                loja.endereco = endereco
                loja.save()

                return JsonResponse(
                    {"detail": f"Loja {loja.nome} atualizada com sucesso"}, status=200
                )
            else:
                # Envia os dados atuais da loja e do endereço
                loja_data = {
                    "nome": loja.nome,
                    "descricao": loja.descricao,
                    "rua": loja.endereco.rua,
                    "cidade": loja.endereco.cidade,
                    "estado": loja.endereco.estado,
                    "cep": loja.endereco.cep,
                }
                return JsonResponse(loja_data, status=200)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse(
                {"detail": "Erro ao processar a solicitação", "error": mensagem_erro},
                status=500,
            )

    @permissions.isAutorizado(5, True)
    def excluir_loja(request, id_loja):
        try:
            loja = get_object_or_404(Loja, pk=id_loja)
            loja.delete()
            return JsonResponse({"detail": "Loja excluída com sucesso"}, status=200)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse(
                {"detail": "Erro ao excluir a loja", "error": mensagem_erro}, status=500
            )
