from django.shortcuts import render, get_object_or_404, redirect
from ..utils import utils
from app import models
from ..static import Alerta, UserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from uuid import UUID
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class views_cliente:

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def lista_clientes(request, Alerta=None):
        if utils.get_status(request):
            return render(request, "cliente/lista_clientes.html")
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def criar_cliente(request):
        if utils.get_status(request):
            if request.method == "POST":
                nome_cliente = request.POST.get("nome_cliente")
                telefone = request.POST.get("telefone")
                ultima_compra = request.POST.get("ultima_compra")
                tipo_cliente = request.POST.get("tipo_cliente")
                decricao = request.POST.get("decricao")

                cliente = models.Cliente.objects.create(
                    nome=nome_cliente,
                    telefone=telefone,
                    ultima_compra=ultima_compra,
                    tipo_cliente=tipo_cliente,
                )
                cliente.save()
                return redirect("cliente/lista_clientes")

            else:
                return render(request, "cadastrar_cliente.html")
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def editar_cliente(request, cliente_id):
        if utils.utis.get_status(request):
            cliente = get_object_or_404(models.Cliente, id_cliente=cliente_id)
            if request.method == "POST":
                cliente.nome = request.POST.get("nome_cliente")
                cliente.telefone = request.POST.get("telefone")
                cliente.ultima_compra = request.POST.get("ultima_compra")
                cliente.tipo_cliente = request.POST.get("tipo_cliente")

                cliente.save()
                return redirect("cliente/lista_clientes")
            else:
                return render(request, "editar_cliente.html", {"cliente": cliente})
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def selecionar_cliente(request, cliente_id):
        if utils.get_status(request):
            cliente = get_object_or_404(models.Cliente, id_cliente=cliente_id)
            return render(request, "selecionar_cliente.html", {"cliente": cliente})
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def excluir_cliente(request, cliente_id):
        if utils.get_status(request):
            cliente = get_object_or_404(models.Cliente, id_cliente=cliente_id)
            if request.method == "POST":
                # Lógica para excluir o cliente
                return redirect("cliente/lista_clientes")
            else:
                return render(request, "excluir_cliente.html", {"cliente": cliente})
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def home_cliente(request):
        return render(request, "cliente/default/home.html")

    @staticmethod
    @csrf_exempt
    @utils.verificar_permissoes(codigo_model=8)
    def api_create_update_cliente(request):
        try:
            if request.method == "POST":
                data = json.loads(request.body)
                cliente_id = data.get("id_cliente",None)

                # Verifica se todos os campos obrigatórios de endereço estão presentes
                endereco_data = {
                    "rua": data.get("rua", ""),
                    "numero": data.get("numero", ""),
                    "bairro": data.get("bairro", ""),
                    "cidade": data.get("cidade", ""),
                    "estado": data.get("estado", ""),
                    "codigo_postal": data.get("cep", ""),
                    "descricao": data.get("descricao_endereco", "")
                }
                endereco = None
                if endereco_data["rua"] and endereco_data["numero"] and endereco_data["bairro"]:
                    endereco, created = models.Endereco.objects.update_or_create(
                        rua=endereco_data["rua"],
                        numero=endereco_data["numero"],
                        bairro=endereco_data["bairro"],
                        defaults=endereco_data
                    )

                if cliente_id:
                    # Atualiza o cliente existente
                    cliente = models.Cliente.objects.filter(id_cliente=cliente_id).first()
                    if cliente:
                        cliente.nome = data.get("nome", cliente.nome)
                        cliente.telefone = data.get("telefone", cliente.telefone)
                        cliente.descricao = data.get("descricao", cliente.descricao)
                        cliente.tipo_cliente = data.get("tipo_cliente", cliente.tipo_cliente)
                        cliente.endereco = endereco
                        cliente.save()
                        message = "Cliente e Endereço atualizados com sucesso"
                    else:
                        return JsonResponse({"error": "Cliente não encontrado"}, status=404)
                else:
                    # Cria um novo cliente
                    cliente = models.Cliente.objects.create(
                        nome=data["nome"],
                        telefone=data["telefone"],
                        descricao=data.get("descricao", None),
                        tipo_cliente=data.get("tipo_cliente", None),
                        endereco=endereco,
                       
                        empresa_id=UserInfo.get_id_empresa(request),
                    )
                    message = "Cliente e Endereço inseridos com sucesso"

                # Retorna os dados do cliente
                response_data = {
                    "id_cliente": str(cliente.id_cliente),
                    "nome": cliente.nome,
                    "telefone": cliente.telefone,
                    "descricao": cliente.descricao,
                    "tipo_cliente": cliente.tipo_cliente,
                    "rua": endereco.rua if endereco else None,
                    "numero": endereco.numero if endereco else None,
                    "bairro": endereco.bairro if endereco else None,
                    "cidade": endereco.cidade if endereco else None,
                    "estado": endereco.estado if endereco else None,
                    "cep": endereco.codigo_postal if endereco else None,
                    "descricao": endereco.descricao if endereco else None,
                    "insert": cliente.insert,
                    "empresa_id": cliente.empresa_id,
                }

                return JsonResponse({"data": response_data, "message": message}, status=200 if cliente_id else 201)

        except Exception as e:
            # Retorna uma resposta de erro em caso de exceção
            return JsonResponse({"error": str(e)}, status=400)
    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_get_cliente(request, cliente_id):
        cliente = get_object_or_404(models.Cliente, pk=cliente_id)
        cliente_data = {
            "id_cliente": cliente.pk,
            "nome_cliente": cliente.nome,
            "telefone": cliente.telefone,
            "ultima_compra": cliente.ultima_compra,
            "tipo_cliente": cliente.tipo_cliente,
            "descricao_cliente": cliente.descricao,
            "empresa_id": cliente.empresa_id,
        }
        return JsonResponse(cliente_data)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    @csrf_exempt
    def api_update_cliente(request, cliente_id):
        cliente = get_object_or_404(models.Cliente, pk=cliente_id)
        if request.method == "PUT":
            nome_cliente = request.POST.get("nome_cliente", cliente.nome)
            telefone = request.POST.get("telefone", cliente.telefone)
            ultima_compra = request.POST.get("ultima_compra", cliente.ultima_compra)
            tipo_cliente = request.POST.get("tipo_cliente", cliente.tipo_cliente)
            descricao_cliente = request.POST.get("descricao_cliente", cliente.descricao)
            empresa_id = request.POST.get("empresa_id", cliente.empresa_id)

            cliente.nome = nome_cliente
            cliente.telefone = telefone
            cliente.ultima_compra = ultima_compra
            cliente.tipo_cliente = tipo_cliente
            cliente.descricao = descricao_cliente
            cliente.empresa_id = empresa_id

            cliente.save()

            return JsonResponse({"message": "Cliente atualizado com sucesso"})

        return JsonResponse({"error": "Método não permitido"}, status=405)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_delete_cliente(request, cliente_id):
        cliente = get_object_or_404(models.liente, pk=cliente_id)
        cliente.delete()
        return JsonResponse({"message": "Cliente deletado com sucesso"}, status=204)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_get_clientes_by_empresa(request):
        empresa_id = UserInfo.get_id_empresa(request)

        # Obter clientes da empresa com os dados do endereço
        clientes = models.Cliente.objects.filter(empresa_id=empresa_id).select_related(
            "endereco"
        )

        try:
            # Verificar se não há clientes
            if not clientes:
                return JsonResponse(
                    {
                        "message": "Não foram encontrados clientes para esta empresa.",
                    }
                )

            # Construir a lista de dicionários contendo os dados de cada cliente com sua última venda
            clientes_data = []
            for cliente in clientes:
                try:
                    # Obter a última venda do cliente
                    ultima_venda = (
                        models.Venda.objects.filter(cliente=cliente)
                        .order_by("-insert")
                        .first()
                    )

                    # Construir o dicionário de dados do cliente e sua última venda
                    cliente_data = {
                        "id_cliente": cliente.id_cliente,
                        "nome": cliente.nome,
                        "telefone": cliente.telefone,
                        "descricao": cliente.descricao,
                        "tipo_cliente": cliente.tipo_cliente,
                        "rua": cliente.endereco.rua if cliente.endereco else None,
                        "numero": (
                            cliente.endereco.numero if cliente.endereco else None
                        ),
                        "cep": (
                            cliente.endereco.codigo_postal if cliente.endereco else None
                        ),
                        "estado": (
                            cliente.endereco.estado if cliente.endereco else None
                        ),
                        "bairro": (
                            cliente.endereco.bairro if cliente.endereco else None
                        ),
                        "cidade": (
                            cliente.endereco.cidade if cliente.endereco else None
                        ),
                        "descricao_endereco": (
                            cliente.endereco.descricao if cliente.endereco else None
                        ),
                        "ultima_venda": {
                            "descricao": (
                                ultima_venda.descricao if ultima_venda else None
                            ),
                            "data_venda": (
                                ultima_venda.data_venda if ultima_venda else None
                            ),
                            "forma_pagamento": (
                                ultima_venda.forma_pagamento if ultima_venda else None
                            ),
                            "valor_total": (
                                str(ultima_venda.valor_total) if ultima_venda else None
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
                    clientes_data.append(cliente_data)
                except Exception as e:
                    # Lidar com exceções ao acessar os atributos do cliente ou da venda
                    print(f"Erro ao processar cliente {cliente.id_cliente}: {e}")
                    continue

            return JsonResponse({"clientes": clientes_data, "success": True})
        except Exception as e:
            # Lidar com exceções gerais
            return JsonResponse(
                {
                    "message": f"Ocorreu um erro ao processar a solicitação: {e}",
                }
            )

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_get_cliente(request):
        empresa_id = UserInfo.get_id_empresa(
            request
        )  # Obtenha o ID da empresa do usuário
        # Obtenha os clientes da empresa com os dados do endereço
        clientes = models.Cliente.objects.filter(empresa_id=empresa_id).select_related(
            "endereco"
        )
        # Construa a lista de dicionários contendo os dados de cada cliente
        clientes_data = []
        for cliente in clientes:
            data = {
                "id_cliente": str(cliente.id_cliente),
                "nome": cliente.nome,
                "telefone": cliente.telefone,
                "descricao": cliente.descricao,
                "tipo_cliente": cliente.tipo_cliente,
                "rua": cliente.endereco.rua,
                "numero": cliente.endereco.numero,
                "cep": cliente.endereco.codigo_postal,
                "estado": cliente.endereco.estado,
                "bairro": cliente.endereco.bairro,
                "cidade": cliente.endereco.cidade,
                "descricao_endereco": cliente.endereco.descricao,
            }
            clientes_data.append(data)

        # Retorne a resposta JSON com os dados dos clientes
        return JsonResponse({"data": clientes_data, "sucess": "true"})

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_get_vendas_by_cliente(request, id_cliente):
        try:
            # Convertendo o campo 'insert' para um campo de data e ordenando pelos mais recentes
            vendas = (
                models.Venda.objects.filter(cliente_id=id_cliente)
                .annotate(insert_date=Cast(F("insert"), output_field=DateTimeField()))
                .order_by("-insert_date")
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

                venda_data = {
                    "id_venda": venda.id_venda,
                    "data_venda": venda.data_venda,
                    "forma_pagamento": venda.forma_pagamento,
                    "estado_transacao": venda.estado_transacao,
                    "metodo_entrega": venda.metodo_entrega,
                    "desconto": venda.desconto,
                    "valor_total": venda.valor_total,
                    "valor_entrega": venda.valor_entrega,
                    "valor_pago": venda.valor_pago,
                    "troco": venda.troco,
                    "insert": venda.insert,
                    "update": venda.update,
                    "descricao": venda.descricao,
                    "usuario": venda.usuario.nome_completo,
                    "loja": venda.loja.nome_loja,
                    "cliente_id": venda.cliente_id,
                    "itens_compra": itens_data,
                }

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
