from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import app.view as view
from ..models import Usuario, PDV, Loja, RegistroDiarioPDV, AssociadoPDV, TransacaoPDV
from app.static import Alerta, UserInfo
from app.utils import Utils


class views_pdv:
    @staticmethod
    @Utils.verificar_permissoes(codigo_model="pdv")
    def pdv(request):
        return render(request, "pdv/lista_pdv.html")

    @Utils.verificar_permissoes(codigo_model="pdv")
    def list_pdv(request, id_loja=None):
        if request.method == "GET":
            try:
                if id_loja != None:
                    pdvs = PDV.objects.filter(loja_id=id_loja)
                else:
                    id_empresa = UserInfo.get_id_empresa(request)
                    pdvs = PDV.objects.filter(loja__empresa_id=id_empresa)
                pdv_list = []
                for pdv in pdvs:
                    pdv_list.append(
                        {
                            "id_pdv": pdv.id_pdv,
                            "nome": pdv.nome,
                            "loja": pdv.loja_id,
                            "insert": pdv.insert,
                            "update": pdv.update,
                            "saldo_inicial": pdv.saldo_inicial,
                            "status_operacao": pdv.status_operacao,
                        }
                    )
                return JsonResponse({"success": True, "data": pdv_list}, status=200)
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @Utils.verificar_permissoes(codigo_model="pdv")
    @csrf_exempt
    def create_pdv(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                nome = data.get("nome", "PDV Padrão")
                loja_id = data.get("id_loja",None)
                saldo_inicial = data.get("saldo_inicial", 100)
                saldo_inicial = Utils.converter_para_decimal(saldo_inicial)
                status_operacao = data.get("status_operacao", True)
                usuario_associado = data.get("id_usuario", None)
                if not usuario_associado:
                    return JsonResponse(
                        {"success": False, "message": "usuario associado ID é obrigatório"},
                        status=400,
                    )
                if not loja_id:
                    return JsonResponse(
                        {"success": False, "message": "Loja ID é obrigatório"},
                        status=400,
                    )

                try:
                    loja = Loja.objects.get(id_loja=loja_id)
                except Loja.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": "Loja não encontrada"}, status=404
                    )

                pdv = PDV.objects.create(
                    nome=nome,
                    loja=loja,
                    saldo_inicial=saldo_inicial,
                    status_operacao=status_operacao,
                )
                id_empresa = UserInfo.get_id_empresa(request)
                usuario = Usuario.objects.get(empresa_id=id_empresa,id=usuario_associado)
                data["usuario"] = usuario.id_usuario
                data["pdv"] = pdv.id_pdv
                views_associado_pdv.create_associado_pdv(request,data)

                #associando admin
                usuario = Usuario.objects.get(empresa_id=id_empresa, nivel_usuario=1)
                data["usuario"] = usuario.id_usuario
                data["pdv"] = pdv.id_pdv
                views_associado_pdv.create_associado_pdv(request,data)
                return JsonResponse(
                    {
                        "success": True,
                        "message": "PDV criado com sucesso",
                        "data": {
                            "id_pdv": pdv.id_pdv,
                            "nome": pdv.nome,
                            "loja": pdv.loja_id,
                            "insert": pdv.insert,
                            "update": pdv.update,
                            "saldo_inicial": pdv.saldo_inicial,
                            "status_operacao": pdv.status_operacao,
                        },
                    },
                    status=201,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"success": False, "message": "JSON inválido"}, status=400
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @Utils.verificar_permissoes(codigo_model="pdv")
    @csrf_exempt
    def update_pdv(request):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)

                pdv_id = data.get("id_pdv")
                nome = data.get("nome")
                loja_id = data.get("loja_id")
                status_operacao = data.get("status_operacao", False)

                try:
                    pdv = PDV.objects.get(id_pdv=pdv_id)
                except PDV.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": "PDV não encontrado"}, status=404
                    )

                if loja_id:
                    try:
                        loja = Loja.objects.get(id_loja=loja_id)
                        pdv.loja = loja
                    except Loja.DoesNotExist:
                        return JsonResponse(
                            {"success": False, "message": "Loja não encontrada"},
                            status=404,
                        )

                if nome is not None:
                    pdv.nome = nome
                if status_operacao is not None:
                    pdv.status_operacao = status_operacao

                pdv.update = Utils.obter_data_hora_atual()
                pdv.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "PDV atualizado com sucesso",
                        "data": {
                            "id_pdv": pdv.id_pdv,
                            "nome": pdv.nome,
                            "loja": pdv.loja_id,
                            "insert": pdv.insert,
                            "update": pdv.update,
                            "saldo_inicial": pdv.saldo_inicial,
                            "status_operacao": pdv.status_operacao,
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"success": False, "message": "JSON inválido"}, status=400
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )


class views_registro_diario_pdv:

    @csrf_exempt
    def list_registro_diario_pdv(request, id_pdv):
        if request.method == "GET":
            try:
                registros = RegistroDiarioPDV.objects.filter(pvd_id=id_pdv)
                registro_list = []
                for registro in registros:
                    registro_list.append(
                        {
                            "id_registro_diario": registro.id_registro_diario,
                            "pdv": registro.pdv.id_pdv,
                            "dia": registro.dia,
                            "saldo_inicial": registro.saldo_inicial,
                            "saldo_final": registro.saldo_final,
                            "status_operacao": registro.status_operacao,
                            "horario_iniciou": registro.horario_iniciou,
                            "horario_fechamento": registro.horario_fechamento,
                            "insert": registro.insert,
                            "update": registro.update,
                        }
                    )
                return JsonResponse(
                    {"success": True, "data": registro_list}, status=200
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @csrf_exempt
    def update_registro_diario_pdv(request, id_registro_diario):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)

                pdv_id = data.get("pdv_id")
                saldo_final = data.get("saldo_final")
                status_operacao = data.get("status_operacao")
                horario_fechamento = data.get("horario_fechamento")

                try:
                    registro_diario = RegistroDiarioPDV.objects.get(
                        id_registro_diario=id_registro_diario
                    )
                except RegistroDiarioPDV.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": "Registro diário não encontrado"},
                        status=404,
                    )

                if pdv_id:
                    try:
                        pdv = PDV.objects.get(id_pdv=pdv_id)
                        registro_diario.pdv = pdv
                    except PDV.DoesNotExist:
                        return JsonResponse(
                            {"success": False, "message": "PDV não encontrado"},
                            status=404,
                        )

                if saldo_final is not None:
                    registro_diario.saldo_final = saldo_final
                if status_operacao is not None:
                    registro_diario.status_operacao = status_operacao
                if horario_fechamento is not None:
                    registro_diario.horario_fechamento = horario_fechamento

                registro_diario.update = Utils.obter_data_hora_atual()
                registro_diario.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Registro diário atualizado com sucesso",
                        "data": {
                            "id_registro_diario": registro_diario.id_registro_diario,
                            "pdv": registro_diario.pdv.id_pdv,
                            "dia": registro_diario.dia,
                            "saldo_inicial": registro_diario.saldo_inicial,
                            "saldo_final": registro_diario.saldo_final,
                            "status_operacao": registro_diario.status_operacao,
                            "horario_iniciou": registro_diario.horario_iniciou,
                            "horario_fechamento": registro_diario.horario_fechamento,
                            "insert": registro_diario.insert,
                            "update": registro_diario.update,
                        },
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {"success": False, "message": "JSON inválido"}, status=400
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )


class views_associado_pdv:

    @csrf_exempt
    def list_associado_pdv(request):
        if request.method == "GET":
            try:
                associados = AssociadoPDV.objects.all()
                associado_list = []
                for associado in associados:
                    associado_list.append(
                        {
                            "id_associado": associado.id_associado,
                            "insert": associado.insert,
                            "update": associado.update,
                            "status_acesso": associado.status_acesso,
                            "usuario": (
                                associado.usuario_id if associado.usuario else None
                            ),
                            "pdv": associado.pdv.id_pdv if associado.pdv else None,
                        }
                    )
                return JsonResponse(
                    {"success": True, "data": associado_list}, status=200
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @csrf_exempt
    def create_associado_pdv(request, data):
        if request.method == "POST":
            try:

                usuario = Usuario.objects.get(id_usuario=data["usuario"])
                pdv = PDV.objects.get(id_pdv=data["pdv"])
                associado = AssociadoPDV.objects.create(
                    usuario=usuario,
                    pdv=pdv,
                    status_acesso=data.get("status_acesso", True),
                )
                associado.save()
                return JsonResponse(
                    {"success": True, "data": {"id_associado": associado.id_associado}},
                    status=201,
                )
            except Usuario.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Usuário não encontrado"}, status=404
                )
            except PDV.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "PDV não encontrado"}, status=404
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @csrf_exempt
    def update_associado_pdv(request):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                associado = AssociadoPDV.objects.get(id_associado=data["id_associado"])

                if "status_acesso" in data:
                    associado.status_acesso = data["status_acesso"]
                if "usuario" in data:
                    associado.usuario = Usuario.objects.get(id_usuario=data["usuario"])
                if "pdv" in data:
                    associado.pdv = PDV.objects.get(id_pdv=data["pdv"])

                associado.save()
                return JsonResponse(
                    {"success": True, "data": {"id_associado": associado.id_associado}},
                    status=200,
                )
            except AssociadoPDV.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "AssociadoPDV não encontrado"},
                    status=404,
                )
            except Usuario.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "Usuário não encontrado"}, status=404
                )
            except PDV.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "PDV não encontrado"}, status=404
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )


class views_transacao_pdv:

    @staticmethod
    @Utils.verificar_permissoes(codigo_model="transacao")
    def lista_transacao(request):

        return render(request, "caixa/transacao/lista_transacao.html")
