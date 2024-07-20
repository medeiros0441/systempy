from django.shortcuts import render, get_object_or_404, redirect
from api.utils import Utils
from api import models
from api.static import Alerta, UserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import api.view as view


class views_cliente:

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    def lista_clientes(request, Alerta=None):
        return render(request, "cliente/lista_clientes.html")

    @Utils.verificar_permissoes(8, True)
    def criar_cliente(request):
        if Utils.get_status(request):
            if request.method == "POST":
                status, msg = views_cliente.create_cliente_data(request.POST)
                return redirect("cliente/lista_clientes")
            else:
                return render(request, "cadastrar_cliente.html")
        else:
            return view.views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    @Utils.verificar_permissoes(8, True)
    def editar_cliente(request, cliente_id):
        cliente = get_object_or_404(models.Cliente, id_cliente=cliente_id)
        if request.method == "POST":
            status, msg = views_cliente.update_cliente_data(request.POST)
            cliente.save()
            return redirect("cliente/lista_clientes")
        else:
            return render(request, "editar_cliente.html", {"cliente": cliente})

    @Utils.verificar_permissoes(8, True)
    def selecionar_cliente(request, cliente_id):
        if Utils.get_status(request):
            cliente = get_object_or_404(models.Cliente, id_cliente=cliente_id)
            return render(request, "selecionar_cliente.html", {"cliente": cliente})
        else:
            return view.views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    @Utils.verificar_permissoes(8, True)
    def excluir_cliente(request, cliente_id):
        cliente = get_object_or_404(models.Cliente, id_cliente=cliente_id)
        if request.method == "POST":
            # Lógica para excluir o cliente
            return redirect("cliente/lista_clientes")
        else:
            return render(request, "excluir_cliente.html", {"cliente": cliente})

    @Utils.verificar_permissoes(8, True)
    @csrf_exempt
    def api_create_cliente(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                empresa_id = UserInfo.get_id_empresa(request)

                cliente_data = data.get("cliente", {})
                endereco_data = data.get("endereco", {})
                cliente_data["empresa_id"] = empresa_id
                # Criar o endereço
                endereco, status_endereco, msg_endereco = (
                    view.views_endereco.create_endereco_data(endereco_data)
                )
                if not status_endereco:
                    return JsonResponse(
                        {"success": False, "message": msg_endereco}, status=400
                    )

                # Criar o cliente
                cliente, status_cliente, msg_cliente = (
                    views_cliente.create_cliente_data(
                        cliente_data, endereco.id_endereco
                    )
                )
                if status_cliente:
                    response_data = Utils.modelo_para_json(cliente, endereco)
                    return JsonResponse(
                        {
                            "success": status_cliente,
                            "data": response_data,
                            "message": msg_cliente,
                        }
                    )
                else:
                    return JsonResponse(
                        {"success": False, "message": msg_cliente}, status=400
                    )
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Método não permitido"}, status=405)

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    @csrf_exempt
    def api_update_cliente(request):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)

                cliente_data = data.get("cliente", {})
                endereco_data = data.get("endereco", {})

                if not endereco_data.get("id_endereco"):
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Não foi possível recuperar o id_endereco para atualizar.",
                        },
                        status=400,
                    )

                if not cliente_data.get("id_cliente"):
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Não foi possível recuperar o id_cliente para atualizar.",
                        },
                        status=400,
                    )
                endereco, status_endereco, msg_endereco = (
                    view.views_endereco.update_endereco_data(
                        endereco_data["id_endereco"], endereco_data
                    )
                )
                if not status_endereco:
                    return JsonResponse(
                        {"success": False, "message": msg_endereco}, status=400
                    )

                obj, status, msg = views_cliente.update_cliente_data(
                    cliente_data["id_cliente"], cliente_data
                )
                if status:
                    return JsonResponse(
                        {
                            "success": status,
                            "data": Utils.modelo_para_json(obj),
                            "message": msg,
                        }
                    )
                else:
                    return JsonResponse({"success": status, "message": msg}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Método não permitido"}, status=405)

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    def api_get_cliente(request, cliente_id):
        cliente = get_object_or_404(models.Cliente, pk=cliente_id)
        return JsonResponse({"success": True, "data": Utils.modelo_para_json(cliente)})

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    def api_delete_cliente(request, cliente_id):
        try:
            empresa_id = UserInfo.get_id_empresa(request)
            cliente = models.Cliente.objects.get(
                id_cliente=cliente_id, empresa_id=empresa_id
            )

            if cliente:
                cliente.delete()
                return JsonResponse(
                    {"success": True, "message": "Cliente excluído com sucesso"}
                )
            else:
                return JsonResponse({"error": "Cliente não encontrado"}, status=404)

        except models.Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente não encontrado"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @Utils.verificar_permissoes(8, True)
    @csrf_exempt
    def api_get_clientes_by_empresa(request):
        empresa_id = UserInfo.get_id_empresa(request)

        # Obter clientes da empresa com os dados do endereço
        clientes = models.Cliente.objects.filter(empresa_id=empresa_id)

        try:
            # Verificar se não há clientes
            if not clientes.exists():
                return JsonResponse(
                    {"message": "Não foram encontrados clientes para esta empresa."},
                    status=404,
                )

            clientes_data = []
            for cliente in clientes:
                try:
                    # Obter a última venda do cliente
                    ultima_venda = (
                        models.Venda.objects.filter(cliente=cliente)
                        .order_by("-insert")
                        .first()
                    )

                    # Obter o endereço do cliente
                    endereco = models.Endereco.objects.filter(
                        id_endereco=cliente.endereco_id
                    ).first()
                    cliente_data = {}
                    # Construir o dicionário de dados do cliente
                    cliente_data = Utils.modelo_para_json(cliente, endereco)
                    cliente_data.update(
                        {
                            "ultima_venda": {
                                "descricao": (
                                    ultima_venda.descricao if ultima_venda else None
                                ),
                                "data_venda": (
                                    ultima_venda.data_venda if ultima_venda else None
                                ),
                                "forma_pagamento": (
                                    ultima_venda.forma_pagamento
                                    if ultima_venda
                                    else None
                                ),
                                "valor_total": (
                                    str(ultima_venda.valor_total)
                                    if ultima_venda
                                    else None
                                ),
                                "produtos": (
                                    [
                                        item.produto.nome
                                        for item in ultima_venda.itemcompra_set.all()
                                    ]
                                    if ultima_venda
                                    else None
                                ),
                            },
                        }
                    )

                    clientes_data.append(cliente_data)
                except Exception as e:
                    print(f"Erro ao processar cliente {cliente.id_cliente}: {e}")

            return JsonResponse({"success": True, "data": clientes_data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    def api_get_cliente(request):
        empresa_id = UserInfo.get_id_empresa(
            request
        )  # Obtenha o ID da empresa do usuário

        # Obtenha os clientes da empresa com os dados do endereço
        clientes = models.Cliente.objects.filter(empresa_id=empresa_id).select_related(
            "endereco"
        )

        try:
            # Verificar se não há clientes
            if not clientes:
                return JsonResponse(
                    {"message": "Não foram encontrados clientes para esta empresa."},
                    status=404,
                )

            # Construa a lista de dicionários contendo os dados de cada cliente
            clientes_data = [Utils.modelo_para_json(cliente) for cliente in clientes]

            # Retorne a resposta JSON com os dados dos clientes
            return JsonResponse({"data": clientes_data, "success": True})
        except Exception as e:
            # Lidar com exceções gerais
            return JsonResponse(
                {"message": f"Ocorreu um erro ao processar a solicitação: {e}"},
                status=500,
            )

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    def api_get_vendas_by_cliente(request, id_cliente):
        try:
            # Convertendo o campo 'insert' para um campo de data e ordenando pelos mais recentes
            vendas = models.Venda.objects.filter(cliente_id=id_cliente).order_by(
                "-insert"
            )
            # Preparar dados para JSON Response
            vendas_data = []

            for venda in vendas:
                itens_compra = models.ItemCompra.objects.filter(venda=venda)
                itens_data = list(
                    itens_compra.values(
                        "id_item_compra",
                        "quantidade",
                        "insert",
                        "update",
                        nome=F("produto__nome"),  # Renomear para "nome"
                    )
                )

                venda_data = Utils.modelo_para_json(venda)
                venda_data.update(
                    {
                        "itens_compra": itens_data,
                        "usuario": venda.usuario.nome_completo,
                        "loja": venda.loja.nome,
                        "cliente_id": venda.cliente_id,
                    }
                )

                vendas_data.append(venda_data)

            return JsonResponse({"data": vendas_data, "success": True})

        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Cliente não encontrado.", "success": False}, status=404
            )
        except ValidationError as e:
            return JsonResponse({"error": str(e), "success": False}, status=400)
        except Exception as e:
            return JsonResponse(
                {
                    "error": "Erro interno no servidor.",
                    "success": False,
                    "details": str(e),
                },
                status=500,
            )

    def create_cliente_data(data, id_endereco):
        """
        Cria uma instância do modelo Cliente com base nos dados fornecidos.
        """
        try:
            if not data["empresa_id"]:
                None, False, "Está faltando o id_empresa."
            cliente = models.Cliente.objects.create(
                nome=data.get("nome", ""),
                telefone=data.get("telefone", ""),
                ultima_compra=data.get("ultima_compra"),
                insert=Utils.obter_data_hora_atual(),
                update=Utils.obter_data_hora_atual(),
                tipo_cliente=data.get("tipo_cliente", ""),
                descricao=data.get("descricao", ""),
                endereco_id=id_endereco,
                empresa_id=data.get("empresa_id"),
            )
            return cliente, True, "Cadastro efetuado com sucesso."
        except Exception as e:
            return None, False, f"Erro ao cadastrar cliente: {str(e)}"

    def update_cliente_data(cliente_id, data):
        """
        Atualiza uma instância existente do modelo Cliente com base nos dados fornecidos.
        """
        try:
            cliente = models.Cliente.objects.get(id_cliente=cliente_id)
            cliente.nome = data.get("nome", cliente.nome)
            cliente.telefone = data.get("telefone", cliente.telefone)
            cliente.ultima_compra = data.get("ultima_compra", cliente.ultima_compra)
            cliente.update = Utils.obter_data_hora_atual()
            cliente.tipo_cliente = data.get("tipo_cliente", cliente.tipo_cliente)
            cliente.descricao = data.get("descricao", cliente.descricao)
            cliente.save()
            return cliente, True, "Atualização efetuada."
        except models.Cliente.DoesNotExist:
            return None, False, f"Cliente com ID {cliente_id} não encontrado."
        except Exception as e:
            return None, False, f"Erro ao atualizar cliente: {str(e)}"
