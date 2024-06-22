from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import app.view as view
from ..models import (
    Usuario,
    PDV,
    Loja,
    RegistroDiarioPDV,
    AssociadoPDV,
    TransacaoPDV,
    Associado,
    Personalizacao,
)
from app.static import Alerta, UserInfo
from app.utils import Utils


class views_pdv:
    @staticmethod
    @Utils.verificar_permissoes("pdv", True)
    def pdv(request):
        return render(request, "pdv/lista_pdv.html")

    @Utils.verificar_permissoes("pdv", True)
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

    @Utils.verificar_permissoes("pdv", True)
    @csrf_exempt
    def create_pdv(request):
        # Verifica se o método da requisição é POST
        if request.method != "POST":
            return JsonResponse(
                {"success": False, "message": "Método não permitido"}, status=405
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "JSON inválido"}, status=400
            )

        nome = data.get("nome", "PDV Padrão")
        loja_id = data.get("id_loja")
        saldo_inicial = data.get("saldo_inicial", 100)
        status_operacao = data.get("status_operacao", 2)
        colaborador_selecionado = data.get("id_usuario")

        # Verifica se o ID da loja foi fornecido
        if not loja_id:
            return JsonResponse(
                {"success": False, "message": "Loja ID é obrigatório"}, status=400
            )

        try:
            loja = Loja.objects.get(id_loja=loja_id)
        except Loja.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Loja não encontrada"}, status=404
            )

        try:
            saldo_inicial = Utils.converter_para_decimal(saldo_inicial)
        except ValueError:
            return JsonResponse(
                {"success": False, "message": "Saldo inicial inválido"}, status=400
            )

        try:
            pdv = PDV.objects.create(
                nome=nome,
                loja=loja,
                saldo_inicial=saldo_inicial,
                status_operacao=status_operacao,
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Erro ao criar PDV: {str(e)}"},
                status=500,
            )

        try:
            id_empresa = UserInfo.get_id_empresa(request)
            list_usuario = Usuario.objects.filter(empresa_id=id_empresa)

            data["pdv"] = pdv.id_pdv

            for usuario in list_usuario:
                try:
                    views_pdv.associar_usuario_pdv(
                        usuario, loja_id, colaborador_selecionado, data, request
                    )
                except Exception as e:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": f"Erro ao associar usuário {usuario.id_usuario} ao PDV: {str(e)}",
                        },
                        status=500,
                    )

            return JsonResponse(
                {"success": True, "message": "PDV criado com sucesso"}, status=201
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Erro ao associar usuários ao PDV: {str(e)}",
                },
                status=500,
            )

    def associar_usuario_pdv(usuario, loja_id, colaborador_selecionado, data, request):
        if usuario.nivel_usuario == 1:
            # Associa administradores ao PDV
            data["usuario"] = usuario.id_usuario
            views_associado_pdv.create_associado_pdv(request, data)

        elif usuario.nivel_usuario == 2:
            # Associa gerentes ao PDV se estiverem associados à loja
            gerente_associado = Associado.objects.filter(
                loja_id=loja_id, usuario_id=usuario.id_usuario
            ).first()
            if gerente_associado and gerente_associado.status_acesso:
                data["usuario"] = gerente_associado.usuario_id
                views_associado_pdv.create_associado_pdv(request, data)

        elif usuario.nivel_usuario == 3:
            # Associa colaboradores ao PDV se estiverem associados à loja
            colaborador_associado = Associado.objects.filter(
                loja_id=loja_id, usuario_id=usuario.id_usuario
            ).first()
            data["usuario"] = usuario.id_usuario
            if (
                colaborador_associado
                and colaborador_associado.status_acesso
                and colaborador_associado.usuario_id == colaborador_selecionado
            ):
                data["usuario"] = colaborador_associado.usuario_id
                views_associado_pdv.create_associado_pdv(request, data)
            else:
                data["status_acesso"] = False
                views_associado_pdv.create_associado_pdv(request, data)

    @Utils.verificar_permissoes("pdv", True)
    @csrf_exempt
    def update_pdv(request):
        """
        Atualiza um PDV (Ponto de Venda) existente.
        """
        # Verificar se o método é PUT
        if request.method != "PUT":
            return JsonResponse(
                {"success": False, "message": "Método não permitido"}, status=405
            )

        try:
            # Carregar dados do corpo da requisição
            data = json.loads(request.body)

            # Extrair informações do PDV
            pdv_id = data.get("id_pdv")
            nome = data.get("nome", "PDV Padrão")
            loja_id = data.get("id_loja")
            saldo_inicial = Utils.converter_para_decimal(data.get("saldo_inicial", 100))
            status_operacao = data.get("status_operacao", True)
            usuario_associado_id = data.get("id_usuario")

            # Buscar o PDV
            try:
                pdv = PDV.objects.get(id_pdv=pdv_id)
            except PDV.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": "PDV não encontrado"}, status=404
                )

            # Atualizar loja, se fornecida
            if loja_id:
                try:
                    loja = Loja.objects.get(id_loja=loja_id)
                    pdv.loja = loja
                except Loja.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": "Loja não encontrada"}, status=404
                    )

            # Atualizar outros campos do PDV
            pdv.nome = nome
            pdv.saldo_inicial = saldo_inicial
            pdv.status_operacao = status_operacao
            pdv.update = Utils.obter_data_hora_atual()
            pdv.save()

            # Associar usuário ao PDV, se fornecido
            if usuario_associado_id:
                id_empresa = UserInfo.get_id_empresa(request)
                try:
                    usuario_associado = Usuario.objects.get(
                        empresa_id=id_empresa, id=usuario_associado_id
                    )
                except Usuario.DoesNotExist:
                    return JsonResponse(
                        {"success": False, "message": "Usuário não encontrado"},
                        status=404,
                    )

                # Verificar se o usuário já está associado a outro PDV
                associados_filtrados = AssociadoPDV.objects.filter(
                    pdv=pdv, usuario__nivel_usuario__gte=2
                )
                associado_atual = associados_filtrados.first()

                if associado_atual:
                    # Atualizar associação do usuário ao PDV
                    if (
                        associado_atual.usuario.id_usuario
                        != usuario_associado.id_usuario
                    ):
                        if AssociadoPDV.objects.filter(
                            usuario_id=usuario_associado_id
                        ).exists():
                            return JsonResponse(
                                {
                                    "success": False,
                                    "message": "Usuário não pode estar associado a dois pontos de venda, remova do ponto atual, para inserir associar ao novo.",
                                },
                                status=400,
                            )
                        data2 = {
                            "usuario": usuario_associado.id_usuario,
                            "pdv": pdv.id_pdv,
                            "id_associado": associado_atual.id_associado,
                        }
                        views_associado_pdv.update_associado_pdv(request, data2)
                else:
                    # Criar nova associação do usuário ao PDV
                    data2 = {
                        "usuario": usuario_associado.id_usuario,
                        "pdv": pdv.id_pdv,
                    }
                    request.method = "POST"
                    views_associado_pdv.create_associado_pdv(request, data2)
            else:
                # Remover associação do usuário ao PDV
                associados_filtrados = AssociadoPDV.objects.filter(
                    pdv=pdv, usuario__nivel_usuario__gte=2
                )
                associado_atual = associados_filtrados.first()
                if associado_atual:
                    associado_atual.delete()
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "PDV atualizado com sucesso, usuário removido.",
                        },
                        status=200,
                    )

            return JsonResponse(
                {"success": True, "message": "PDV atualizado com sucesso"}, status=200
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)


class views_registro_diario_pdv:

    @Utils.verificar_permissoes("RegistroDiarioPDV", True)
    @csrf_exempt
    def list_registro_diario_pdv(request, id_pdv):
        if request.method == "GET":
            try:
                id_empresa = UserInfo.get_id_empresa(request)
                registros = RegistroDiarioPDV.objects.filter(
                    pdv_id=id_pdv, pdv__loja__empresa_id=id_empresa
                )
                registro_list = Utils.modelos_para_lista_json(registros)
                return JsonResponse(
                    {"success": True, "data": registro_list}, status=200
                )
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @Utils.verificar_permissoes("RegistroDiarioPDV", True)
    @csrf_exempt
    def create_registro_diario_pdv(request, id=None):
        if request.method != "POST":
            return JsonResponse(
                {"success": False, "message": "Método não permitido"}, status=405
            )
        try:
            if id is None:
                data = json.loads(request.body)
                id = data.get("id_pdv")

            if not id:
                return JsonResponse(
                    {"success": False, "message": "ID do PDV não fornecido"}, status=400
                )

            id_empresa = UserInfo.get_id_empresa(request)
            pdv = PDV.objects.get(id_pdv=id, loja__empresa_id=id_empresa)

            data_atual = Utils.obter_data_hora_atual(True)

            registro, created = RegistroDiarioPDV.objects.get_or_create(
                pdv_id=id,
                dia=data_atual,
                defaults={
                    "saldo_inicial_dinheiro": pdv.saldo_inicial,
                    "horario_iniciou": Utils.obter_data_hora_atual(False),
                    "horario_fechamento": None,
                    "saldo_final_dinheiro": 0.00,
                    "saldo_final_total": 0.00,
                    "maquina_tipo": 0.00,
                    "saldo_final_maquina": 0.00,
                },
            )

            if created:
                message = "Registro diário criado com sucesso"
                pdv.status_operacao = True
            else:
                message = "Registro diário atualizado com sucesso"
                pdv.status_operacao = False

            pdv.save()

            return JsonResponse({"success": True, "message": message}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse(
                {"success": False, "message": "PDV ou empresa não encontrados"},
                status=404,
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Erro: {str(e)}"}, status=500
            )

    @Utils.verificar_permissoes("RegistroDiarioPDV", True)
    @csrf_exempt
    def update_status_registro_diario_pdv(request, id=None):
        if request.method != "PUT":
            return JsonResponse(
                {"success": False, "message": "Método não permitido"}, status=405
            )

        try:
            if id is None:
                data = json.loads(request.body)
                id = data.get("id_pdv")

            if not id:
                return JsonResponse(
                    {"success": False, "message": "ID do PDV não fornecido"}, status=400
                )

            id_empresa = UserInfo.get_id_empresa(request)
            pdv = PDV.objects.get(id_pdv=id, loja__empresa_id=id_empresa)
            data_atual = Utils.obter_data_hora_atual(True)
            if pdv.status_operacao:
                exist = RegistroDiarioPDV.objects.get(pdv_id=id).exist()
                # se não existir um registro com base  no status atual do  pdv.status_operacao se for true
                # siginifica que ja tem uma ativo no momento, caso for fale fazmos a  conta dos
                if exist == False:
                    RegistroDiarioPDV.objects.create(
                        pdv=pdv,
                        dia=Utils.obter_data_hora_atual(True),
                        update=Utils.obter_data_hora_atual(),
                    )

            if RegistroDiarioPDV.objects.get(pdv_id=id, dia=data_atual).exist:
                message = "Registro diário finalizado com sucesso"
                pdv.status_operacao = False

            else:
                message = "PDV Em Operção, Registro diário criado com sucesso!"
                pdv.status_operacao = True
            pdv.save
            return JsonResponse({"success": True, "message": message}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse(
                {"success": False, "message": "PDV ou empresa não encontrados"},
                status=404,
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    @Utils.verificar_permissoes("RegistroDiarioPDV", True)
    @csrf_exempt
    def update_registro_diario_pdv(request):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)

                pdv_id = data.get("pdv_id")
                saldo_final = data.get("saldo_final")
                status_operacao = data.get("status_operacao")
                horario_fechamento = data.get("horario_fechamento")
                id_registro_diario = data.get("id_registro_diario")
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


class views_transacao_pdv:

    @staticmethod
    @Utils.verificar_permissoes("transacao", True)
    def lista_transacao(request):
        return render(request, "caixa/transacao/lista_transacao.html")


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
    @Utils.verificar_permissoes(0, True)
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
    def update_associado_pdv(request, data):
        if request.method == "PUT":
            try:
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
