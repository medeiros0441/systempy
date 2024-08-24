import json
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from api.models import (
    UsuarioModel,
    PdvModel,
    LojaModel,
    RegistroDiarioPdvModel,
    AssociadoPdvModel,
    TransacaoPdvModel,
    AssociadoModel,
    PersonalizacaoModel,
    VendaModel,
)
from api.user import UserInfo
from api.utils import Utils
from api.async_processos.pdv import processos_pdv 
from django.db.models import Q
from api.permissions import permissions,CustomPermission
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.services import  PdvService,RegistroDiarioPdvService,TransacaoPdvService,AssociadoPdvService

class PdvView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="pdv", auth_required=True)]
 
    def list_pdv(request, id_loja=None, id_empresa=None):
        if request.method == "GET":
            try:
                if id_loja is not None:
                    pdvs = PdvModel.objects.filter(
                        Q(loja_id=id_loja) & Q(status_operacao__gt=1)
                    )
                else:
                    if id_empresa is None:
                        id_empresa = UserInfo.get_id_empresa(request)
                    pdvs = PdvModel.objects.filter(
                        Q(loja__empresa_id=id_empresa) & Q(status_operacao__gt=0)
                    )

                pdv_list = Utils.modelos_para_lista_json(pdvs)
                return Response({"success": True, "data": pdv_list}, status=200)
            except Exception as e:
                return Response({"success": False, "message": str(e)}, status=500)

        return Response(
            {"success": False, "message": "Método não permitido"}, status=405
        )
 
    def create_pdv(request):
        # Verifica se o método da requisição é POST
        if request.method != "POST":
            return Response(
                {"success": False, "message": "Método não permitido"}, status=405
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response(
                {"success": False, "message": "JSON inválido"}, status=400
            )

        nome = data.get("nome", "PDV Padrão")
        loja_id = data.get("id_loja")
        saldo_inicial = data.get("saldo_inicial", 100)
        status_operacao = int(data.get("status_operacao", 2))
        colaboradores_selecionados = data.get("usuarios_associados", [])

        # Verifica se o ID da loja foi fornecido
        if not loja_id:
            return Response(
                {"success": False, "message": "Loja ID é obrigatório"}, status=400
            )

        try:
            loja = LojaModel.objects.get(id_loja=loja_id)
        except LojaModel.DoesNotExist:
            return Response(
                {"success": False, "message": "Loja não encontrada"}, status=404
            )

        try:
            saldo_inicial = Utils.converter_para_decimal(saldo_inicial)
        except ValueError:
            return Response(
                {"success": False, "message": "Saldo inicial inválido"}, status=400
            )

        try:
            pdv = PdvModel.objects.create(
                nome=nome,
                loja=loja,
                saldo_inicial=saldo_inicial,
                status_operacao=status_operacao,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"Erro ao criar PDV: {str(e)}"},
                status=500,
            )

        try:
            id_empresa = UserInfo.get_id_empresa(request)
            list_usuario = UsuarioModel.objects.filter(empresa_id=id_empresa)

            data["pdv"] = pdv.id_pdv

            for usuario in list_usuario:
                try:
                    PdvView.associar_usuario_pdv(
                        usuario, loja_id, colaboradores_selecionados, data, request
                    )
                except Exception as e:
                    return Response(
                        {
                            "success": False,
                            "message": f"Erro ao associar usuário {usuario.id_usuario} ao PDV: {str(e)}",
                        },
                        status=500,
                    )

            return Response(
                {"success": True, "message": "PDV criado com sucesso"}, status=201
            )
        except Exception as e:
            return Response(
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
            AssociadoPdvView.create_associado_pdv(request, data)
        elif usuario.nivel_usuario == 2:
            # Associa gerentes ao PDV se estiverem associados à loja
            gerente_associado = AssociadoModel.objects.filter(
                loja_id=loja_id, usuario_id=usuario.id_usuario
            ).first()
            if gerente_associado and gerente_associado.status_acesso:
                data["usuario"] = gerente_associado.usuario_id
                AssociadoPdvView.create_associado_pdv(request, data)
        elif usuario.nivel_usuario == 3:
            # Associa colaboradores ao PDV se estiverem associados à loja
            colaborador_associado = AssociadoModel.objects.filter(
                loja_id=loja_id, usuario_id=usuario.id_usuario
            ).first()
            if colaborador_associado and colaborador_associado.status_acesso:
                data["usuario"] = colaborador_associado.usuario_id
                if colaborador_associado.usuario_id in colaboradores_selecionados:
                    AssociadoPdvView.create_associado_pdv(request, data)
                else:
                    data["status_acesso"] = False
                    AssociadoPdvView.create_associado_pdv(request, data)

 
    def update_pdv(request):
        """
        Atualiza um PDV (Ponto de Venda) existente.
        """
        # Verificar se o método é PUT
        if request.method != "PUT":
            return Response(
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
                pdv = PdvModel.objects.get(id_pdv=pdv_id)
            except PdvModel.DoesNotExist:
                return Response(
                    {"success": False, "message": "PDV não encontrado"}, status=404
                )

            # Atualizar loja, se fornecida
            if loja_id:
                try:
                    loja = LojaModel.objects.get(id_loja=loja_id)
                    pdv.loja = loja
                except LojaModel.DoesNotExist:
                    return Response(
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
            associados_atuais = AssociadoPdvModel.objects.filter(pdv=pdv)
            ids_associados_atuais = list(
                associados_atuais.values_list("usuario_id", flat=True)
            )

            # Adicionar novas associações e manter as existentes
            for usuario_associado_id in usuarios_associados:
                if usuario_associado_id not in ids_associados_atuais:
                    try:
                        usuario_associado = UsuarioModel.objects.get(
                            empresa_id=id_empresa, id_usuario=usuario_associado_id
                        )
                        # Criar nova associação do usuário ao PDV
                        AssociadoPdvModel.objects.create(usuario=usuario_associado, pdv=pdv)
                    except UsuarioModel.DoesNotExist:
                        return Response(
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
                        usuario = UsuarioModel.objects.get(
                            id_usuario=associado_atual.usuario_id
                        )
                        if usuario.nivel_usuario == 3:
                            associado_atual.delete()
                    except UsuarioModel.DoesNotExist:
                        pass

            return Response(
                {"success": True, "message": "PDV atualizado com sucesso"}, status=200
            )

        except json.JSONDecodeError:
            return Response(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=500)

    def verificar_status_pdv(pdv):
        if pdv.status_operacao == PdvModel.EXCLUIDO:
            return False, "O PDV foi excluído e não pode ter alterações.", 403
        if pdv.status_operacao == PdvModel.BLOQUEADO:
            return False, "O PDV está bloqueado para operações.", 403
        return True, "", 200


class RegistroDiarioPdvView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="registro_diario_pdv", auth_required=True)]


    @permissions.isAutorizado("RegistroDiarioPDV", True)
    def list_registro_diario_pdv(request, id_pdv):
        if request.method == "GET":
            try:
                id_empresa = UserInfo.get_id_empresa(request)
                registros = RegistroDiarioPdvModel.objects.filter(
                    pdv_id=id_pdv, pdv__loja__empresa_id=id_empresa
                )
                registro_list = Utils.modelos_para_lista_json(registros)
                return Response(
                    {"success": True, "data": registro_list}, status=200
                )
            except Exception as e:
                return Response({"success": False, "message": str(e)}, status=500)

        return Response(
            {"success": False, "message": "Método não permitido"}, status=405
        )

    @permissions.isAutorizado("RegistroDiarioPDV", True)
    def create_registro_diario_pdv(request, id=None):
        if request.method != "POST":
            return Response(
                {"success": False, "message": "Método não permitido"}, status=405
            )
        try:
            if id is None:
                data = json.loads(request.body)
                id = data.get("id_pdv")
            if not id:
                return Response(
                    {"success": False, "message": "ID do PDV não fornecido"}, status=400
                )

            id_empresa = UserInfo.get_id_empresa(request)
            pdv = PdvModel.objects.get(id_pdv=id, loja__empresa_id=id_empresa)
            id_usuario = UserInfo.get_id_usuario(request)
            usuario = UsuarioModel.objects.get(pk=id_usuario)
            status, message = processos_pdv.abrir_registro_diario(pdv, usuario)
            return Response({"success": status, "message": message}, status=200)

        except ObjectDoesNotExist:
            return Response(
                {"success": False, "message": "PDV ou empresa não encontrados"},
                status=404,
            )
        except json.JSONDecodeError:
            return Response(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return Response(
                {"success": False, "message": f"Erro: {str(e)}"}, status=500
            )

    def GetRegistroPdvAberto(pdv_id):
        today = Utils.obter_data_hora_atual("date")
        if pdv_id:
            registro_diario_aberto = RegistroDiarioPdvModel.objects.filter(
                pdv_id=pdv_id, dia=today, horario_fechamento__isnull=True
            ).first()
            if registro_diario_aberto:
                return True, registro_diario_aberto
            return False, None
        return False, None

    @permissions.isAutorizado("RegistroDiarioPDV", True)
    def update_status_registro_diario_pdv(self, request, pdv_id=None):
        if request.method != "PUT":
            return Response(
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
                return Response(
                    {
                        "success": False,
                        "message": "ID do PDV ou ID do usuário não fornecido",
                    },
                    status=400,
                )

            pdv = PdvModel.objects.get(id_pdv=pdv_id)
            status_pdv, mensagem, status_code = PdvView.verificar_status_pdv(pdv)
            if not status_pdv:
                return Response(
                    {"success": False, "message": mensagem}, status=status_code
                )

            if pdv.status_operacao == 2 or pdv.status_operacao == 1:
                status_registro, registro_diario_aberto = self.GetRegistroPdvAberto(
                    pdv.id_pdv
                )
                status_associado, associado = (
                    AssociadoPdvService.UsuarioIsAssociadoInPDV(usuario_id, pdv.id_pdv)
                )

                if not status_associado:
                    return Response(
                        {"success": False, "message": associado}, status=403
                    )

                if status_registro:
                    processos_pdv.fechar_registro_diario(registro_diario_aberto)
                    message = "Registro diário finalizado com sucesso!"
                else:
                    processos_pdv.abrir_registro_diario(pdv)
                    message = "Registro diário criado com sucesso!"

                return Response({"success": True, "message": message}, status=200)

        except ObjectDoesNotExist:
            return Response(
                {"success": False, "message": "PDV ou empresa não encontrados"},
                status=404,
            )
        except json.JSONDecodeError:
            return Response(
                {"success": False, "message": "JSON inválido"}, status=400
            )
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=500)

    @permissions.isAutorizado("RegistroDiarioPDV", True)
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
                    registro_diario = RegistroDiarioPdvModel.objects.get(
                        id_registro_diario=id_registro_diario
                    )
                except RegistroDiarioPdvModel.DoesNotExist:
                    return Response(
                        {"success": False, "message": "Registro diário não encontrado"},
                        status=404,
                    )

                if pdv_id:
                    try:
                        pdv = PdvModel.objects.get(id_pdv=pdv_id)
                        registro_diario.pdv = pdv
                    except PdvModel.DoesNotExist:
                        return Response(
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

                return Response(
                    {
                        "success": True,
                        "message": "Registro diário atualizado com sucesso",
                    },
                    status=200,
                )

            except json.JSONDecodeError:
                return Response(
                    {"success": False, "message": "JSON inválido"}, status=400
                )
            except Exception as e:
                return Response({"success": False, "message": str(e)}, status=500)

        return Response(
            {"success": False, "message": "Método não permitido"}, status=405
        )


class TransacaoPdvView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="transacao_pdv", auth_required=True)]


    def processar_trasacao_pdv(self, request, venda):
        """
        Processa uma venda com base na forma de pagamento e cria as transações PDV apropriadas.
        """
        data = {}

        data["venda_id"] = venda.id_venda
        data["usuario_id"] = Utils.get_id_usuario(request)
        usuario_id = data["usuario_id"]
        registro_diario_id = AssociadoPdvView.get_registro_diario_id(usuario_id)

        if not registro_diario_id:
            return False, "Erro ao obter registro diário"

        RegistroDiarioPdvModel.objects.get(pk=registro_diario_id)

        data["registro_diario_id"] = registro_diario_id

        if venda.tipo_pagamento == 1:
            """Processa a entrada de dinheiro no PDV."""
            data["descricao"] = "ENTRADA EM DINHEIRO, PARA PAGAMENTO."
            data["valor"] = venda.valor_total
            data["tipo_operacao"] = 1  # Tipo de operação para entrada
            processos_pdv.processar_transacao_PDV(data)
            if venda.troco:
                """Processa a retirada de troco no PDV."""
                data["descricao"] = "RETIRADO VALOR EM DINHEIRO PARA TROCO."
                data["valor"] = venda.troco
                data["tipo_operacao"] = 2  # Tipo de operação para retirada
                processos_pdv.processar_transacao_PDV(data)
        else:
            tipo_pagamento_str = venda.get_tipo_pagamento_display()
            """Processa a entrada de valores via máquina no PDV."""
            data["descricao"] = f"ENTRADA DE RECIBO PAGAMENTO VIA {tipo_pagamento_str}"
            data["valor"] = venda.valor_total
            data["tipo_operacao"] = 1  # Tipo de operação para entrada
            processos_pdv.processar_transacao_PDV(data)
        return True, "Processamento de venda concluído com sucesso"


class AssociadoPdvView(viewsets.ViewSet):
    permission_classes = [CustomPermission(codigo_model="associado_pdv", auth_required=True)]


    @action(detail=False, methods=['get'])
    def list_associado_pdv(self, request):
        success, result = AssociadoPdvService.list_associado_pdv()
        if success:
            data = [item.to_dict() for item in result]  # Converta para dict ou formate conforme necessário
            return Response({"success": True, "data": data}, status=200)
        return Response({"success": False, "message": result}, status=500)

    @action(detail=False, methods=['POST'])
    def create_associado_pdv(self, request):
        data = request.data
        success, result = AssociadoPdvService.create_associado_pdv(data)
        if success:
            return Response({"success": True, "data": result}, status=201)
        return Response({"success": False, "message": result}, status=404)

    @action(detail=False, methods=['PUT'])
    def update_associado_pdv(self, request):
        data = request.data
        success, result = AssociadoPdvService.update_associado_pdv(data)
        if success:
            return Response({"success": True, "data": result}, status=200)
        return Response({"success": False, "message": result}, status=404)
 
