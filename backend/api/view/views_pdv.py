from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..models import (
    Usuario,
    PDV,
    Loja,
    RegistroDiarioPDV,
    AssociadoPDV,
    TransacaoPDV,
    Associado,
    Personalizacao,
    Venda,
)
from api.user import UserInfo
from api.utils import Utils
from ..processos.pdv import processos_pdv
from .views_personalizacao import views_personalizacao
from django.db.models import Q
from api.permissions import permissions

class views_pdv:
    @staticmethod
    @permissions.isAutorizado("pdv", True)
    def pdv(request):
        return render(request, "pdv/lista_pdv.html")

    @permissions.isAutorizado("pdv", True)
    @csrf_exempt
    def list_pdv(request, id_loja=None, id_empresa=None):
        if request.method == "GET":
            try:
                if id_loja is not None:
                    pdvs = PDV.objects.filter(
                        Q(loja_id=id_loja) & Q(status_operacao__gt=1)
                    )
                else:
                    if id_empresa is None:
                        id_empresa = UserInfo.get_id_empresa(request)
                    pdvs = PDV.objects.filter(
                        Q(loja__empresa_id=id_empresa) & Q(status_operacao__gt=0)
                    )

                pdv_list = Utils.modelos_para_lista_json(pdvs)
                return JsonResponse({"success": True, "data": pdv_list}, status=200)
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

        return JsonResponse(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @permissions.isAutorizado("pdv", True)
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
        status_operacao = int(data.get("status_operacao", 2))
        colaboradores_selecionados = data.get("usuarios_associados", [])

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
                        usuario, loja_id, colaboradores_selecionados, data, request
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

    def associar_usuario_pdv(
        usuario, loja_id, colaboradores_selecionados, data, request
    ):
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
            if colaborador_associado and colaborador_associado.status_acesso:
                data["usuario"] = colaborador_associado.usuario_id
                if colaborador_associado.usuario_id in colaboradores_selecionados:
                    views_associado_pdv.create_associado_pdv(request, data)
                else:
                    data["status_acesso"] = False
                    views_associado_pdv.create_associado_pdv(request, data)

    @permissions.isAutorizado("pdv", True)
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
            status_operacao = int(data.get("status_operacao"))
            usuarios_associados = data.get("usuarios_associados", [])

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

            id_empresa = UserInfo.get_id_empresa(request)

            # Obter associações atuais do PDV
            associados_atuais = AssociadoPDV.objects.filter(pdv=pdv)
            ids_associados_atuais = list(
                associados_atuais.values_list("usuario_id", flat=True)
            )

            # Adicionar novas associações e manter as existentes
            for usuario_associado_id in usuarios_associados:
                if usuario_associado_id not in ids_associados_atuais:
                    try:
                        usuario_associado = Usuario.objects.get(
                            empresa_id=id_empresa, id_usuario=usuario_associado_id
                        )
                        # Criar nova associação do usuário ao PDV
                        AssociadoPDV.objects.create(usuario=usuario_associado, pdv=pdv)
                    except Usuario.DoesNotExist:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": f"Usuário {usuario_associado_id} não encontrado",
                            },
                            status=404,
                        )

            # Remover associações de usuários que não estão mais na lista fornecida
            for associado_atual in associados_atuais:
                if str(associado_atual.usuario_id) not in usuarios_associados:
                    try:
                        usuario = Usuario.objects.get(
                            id_usuario=associado_atual.usuario_id
                        )
                        if usuario.nivel_usuario == 3:
                            associado_atual.delete()
                    except Usuario.DoesNotExist:
                        pass

            return JsonResponse(
                {"success": True, "message": "PDV atualizado com sucesso"}, status=200
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    def verificar_status_pdv(pdv):
        if pdv.status_operacao == PDV.EXCLUIDO:
            return False, "O PDV foi excluído e não pode ter alterações.", 403
        if pdv.status_operacao == PDV.BLOQUEADO:
            return False, "O PDV está bloqueado para operações.", 403
        return True, "", 200


class views_registro_diario_pdv:

    @permissions.isAutorizado("RegistroDiarioPDV", True)
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

    @permissions.isAutorizado("RegistroDiarioPDV", True)
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
            id_usuario = UserInfo.get_id_usuario(request)
            usuario = Usuario.objects.get(pk=id_usuario)
            status, message = processos_pdv.abrir_registro_diario(pdv, usuario)
            return JsonResponse({"success": status, "message": message}, status=200)

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

    def GetRegistroPdvAberto(pdv_id):
        today = Utils.obter_data_hora_atual("date")
        if pdv_id:
            registro_diario_aberto = RegistroDiarioPDV.objects.filter(
                pdv_id=pdv_id, dia=today, horario_fechamento__isnull=True
            ).first()
            if registro_diario_aberto:
                return True, registro_diario_aberto
            return False, None
        return False, None

    @permissions.isAutorizado("RegistroDiarioPDV", True)
    @csrf_exempt
    def update_status_registro_diario_pdv(self, request, pdv_id=None):
        if request.method != "PUT":
            return JsonResponse(
                {"success": False, "message": "Método não permitido"}, status=405
            )

        try:
            if pdv_id is None:
                data = json.loads(request.body)
                pdv_id = data.get("pdv_id")
                usuario_id = data.get("usuario_id")
            else:
                usuario_id = UserInfo.get_id_usuario(request)

            if not pdv_id or usuario_id is None:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "ID do PDV ou ID do usuário não fornecido",
                    },
                    status=400,
                )

            pdv = PDV.objects.get(id_pdv=pdv_id)
            status_pdv, mensagem, status_code = views_pdv.verificar_status_pdv(pdv)
            if not status_pdv:
                return JsonResponse(
                    {"success": False, "message": mensagem}, status=status_code
                )

            if pdv.status_operacao == 2 or pdv.status_operacao == 1:
                status_registro, registro_diario_aberto = self.GetRegistroPdvAberto(
                    pdv.id_pdv
                )
                status_associado, associado = (
                    views_associado_pdv.UsuarioIsAssociadoInPDV(usuario_id, pdv.id_pdv)
                )

                if not status_associado:
                    return JsonResponse(
                        {"success": False, "message": associado}, status=403
                    )

                if status_registro:
                    processos_pdv.fechar_registro_diario(registro_diario_aberto)
                    message = "Registro diário finalizado com sucesso!"
                else:
                    processos_pdv.abrir_registro_diario(pdv)
                    message = "Registro diário criado com sucesso!"

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

    @permissions.isAutorizado("RegistroDiarioPDV", True)
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
    @permissions.isAutorizado("transacao", True)
    def lista_transacao(request):
        return render(request, "caixa/transacao/lista_transacao.html")

    def processar_trasacao_pdv(self, request, venda):
        """
        Processa uma venda com base na forma de pagamento e cria as transações PDV apropriadas.
        """
        data = {}

        data["venda_id"] = venda.id_venda
        data["usuario_id"] = Utils.get_id_usuario(request)
        usuario_id = data["usuario_id"]
        registro_diario_id = views_associado_pdv.get_registro_diario_id(usuario_id)

        if not registro_diario_id:
            return False, "Erro ao obter registro diário"

        RegistroDiarioPDV.objects.get(pk=registro_diario_id)

        data["registro_diario_id"] = registro_diario_id

        if venda.tipo_pagamento == 1:
            self.processar_entrada_dinheiro(data, venda)
            if venda.troco:
                self.processar_retirada_troco(data, venda.troco)
        else:
            tipo_pagamento_str = venda.get_tipo_pagamento_display()
            self.processar_entrada_pg(data, venda.valor_total, tipo_pagamento_str)

        return True, "Processamento de venda concluído com sucesso"

    def processar_entrada_dinheiro(data, venda):
        """
        Processa a entrada de dinheiro no PDV.
        """
        data["descricao"] = "ENTRADA EM DINHEIRO, PARA PAGAMENTO."
        data["valor"] = venda.valor_total
        data["tipo_operacao"] = 1  # Tipo de operação para entrada
        processos_pdv.processar_transacao_PDV(data)

    def processar_retirada_troco(data, troco):
        """
        Processa a retirada de troco no PDV.
        """
        data["descricao"] = "RETIRADO VALOR EM DINHEIRO PARA TROCO."
        data["valor"] = troco
        data["tipo_operacao"] = 2  # Tipo de operação para retirada
        processos_pdv.processar_transacao_PDV(data)

    def processar_entrada_pg(data, valor_total, tipo_pagamento_str):
        """
        Processa a entrada de valores via máquina no PDV.
        """
        data["descricao"] = f"ENTRADA DE RECIBO PAGAMENTO VIA {tipo_pagamento_str}"
        data["valor"] = valor_total
        data["tipo_operacao"] = 1  # Tipo de operação para entrada
        processos_pdv.processar_transacao_PDV(data)


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
    @permissions.isAutorizado(0, True)
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

    def UsuarioIsAssociadoInPDV(id_usuario, id_pdv):
        try:
            associado = AssociadoPDV.objects.get(usuario_id=id_usuario, pdv_id=id_pdv)
            if associado.status_acesso:
                return True, associado
            return False, "Usuário não tem permissão de acesso ao PDV"
        except AssociadoPDV.DoesNotExist:
            return False, "Associação não encontrada"
