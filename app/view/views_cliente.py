from django.shortcuts import render, get_object_or_404, redirect
from ..utils import utils
from ..models.usuario import Usuario
from ..models import Cliente, Configuracao, Usuario, Endereco, Venda
from ..static import Alerta, UserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from uuid import UUID


class views_cliente:

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def lista_clientes(request):
        if get_status(request):
            clientes = Cliente.objects.all()
            return render(
                request, "cliente/lista_clientes.html", {"clientes": clientes}
            )
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def criar_cliente(request):
        if get_status(request):
            if request.method == "POST":
                nome_cliente = request.POST.get("nome_cliente")
                telefone = request.POST.get("telefone")
                ultima_compra = request.POST.get("ultima_compra")
                tipo_cliente = request.POST.get("tipo_cliente")

                cliente = Cliente.objects.create(
                    nome_cliente=nome_cliente,
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
        if get_status(request):
            cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
            if request.method == "POST":
                cliente.nome_cliente = request.POST.get("nome_cliente")
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
        if get_status(request):
            cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
            return render(request, "selecionar_cliente.html", {"cliente": cliente})
        else:
            return utils.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )

    def excluir_cliente(request, cliente_id):
        if get_status(request):
            cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
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
    def api_create_cliente(request):
        try:
            if request.method == "POST":
                data = json.loads(request.body)

                # Cria o objeto Endereco
                endereco = Endereco.objects.create(
                    rua=data["rua"],
                    numero=data["numero"],
                    bairro=data["bairro"],
                    cidade=data["cidade"],
                    estado=data["estado"],
                    codigo_postal=data["cep"],
                    descricao=data["descricao_endereco"],
                )

                # Cria o objeto Cliente associado ao endereço
                cliente = Cliente.objects.create(
                    nome_cliente=data["nome"],
                    telefone_cliente=data["telefone"],
                    descricao_cliente=data.get("descricao", None),
                    tipo_cliente=data.get("tipo_cliente", None),
                    endereco=endereco,
                    insert=timezone.now(),
                    empresa_id=UserInfo.get_id_empresa(request),
                )

                # Retorna os dados do cliente criado
                return JsonResponse(
                    {
                        "data": {
                            "id_cliente": str(cliente.id_cliente),
                            "nome": cliente.nome_cliente,
                            "telefone": cliente.telefone_cliente,
                            "descricao": cliente.descricao_cliente,
                            "tipo_cliente": cliente.tipo_cliente,
                            "rua": endereco.rua,
                            "numero": endereco.numero,
                            "bairro": endereco.bairro,
                            "cidade": endereco.cidade,
                            "estado": endereco.estado,
                            "cep": endereco.codigo_postal,
                            "descricao": endereco.descricao,
                            "insert": cliente.insert.isoformat(),
                            "empresa_id": cliente.empresa_id,
                        },
                        "message": "Cliente e Endereço inseridos com sucesso",
                    },
                    status=201,
                )

        except Exception as e:
            # Retorna uma resposta de erro em caso de exceção
            return JsonResponse({"error": str(e)}, status=400)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_get_cliente(request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        cliente_data = {
            "id_cliente": cliente.pk,
            "nome_cliente": cliente.nome_cliente,
            "telefone_cliente": cliente.telefone_cliente,
            "ultima_compra": cliente.ultima_compra,
            "tipo_cliente": cliente.tipo_cliente,
            "descricao_cliente": cliente.descricao_cliente,
            "empresa_id": cliente.empresa_id,
        }
        return JsonResponse(cliente_data)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    @csrf_exempt
    def api_update_cliente(request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        if request.method == "PUT":
            nome_cliente = request.POST.get("nome_cliente", cliente.nome_cliente)
            telefone_cliente = request.POST.get(
                "telefone_cliente", cliente.telefone_cliente
            )
            ultima_compra = request.POST.get("ultima_compra", cliente.ultima_compra)
            tipo_cliente = request.POST.get("tipo_cliente", cliente.tipo_cliente)
            descricao_cliente = request.POST.get(
                "descricao_cliente", cliente.descricao_cliente
            )
            empresa_id = request.POST.get("empresa_id", cliente.empresa_id)

            cliente.nome_cliente = nome_cliente
            cliente.telefone_cliente = telefone_cliente
            cliente.ultima_compra = ultima_compra
            cliente.tipo_cliente = tipo_cliente
            cliente.descricao_cliente = descricao_cliente
            cliente.empresa_id = empresa_id

            cliente.save()

            return JsonResponse({"message": "Cliente atualizado com sucesso"})

        return JsonResponse({"error": "Método não permitido"}, status=405)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_delete_cliente(request, cliente_id):
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        cliente.delete()
        return JsonResponse({"message": "Cliente deletado com sucesso"}, status=204)

    @staticmethod
    @utils.verificar_permissoes(codigo_model=8)
    def api_get_clientes_by_empresa(request):
        empresa_id = UserInfo.get_id_empresa(request)

        # Obter clientes da empresa com os dados do endereço
        clientes = Cliente.objects.filter(empresa_id=empresa_id).select_related(
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
                        Venda.objects.filter(cliente=cliente)
                        .order_by("-insert")
                        .first()
                    )

                    # Construir o dicionário de dados do cliente e sua última venda
                    cliente_data = {
                        "id_cliente": (cliente.id_cliente),
                        "nome": cliente.nome_cliente,
                        "telefone": cliente.telefone_cliente,
                        "descricao": cliente.descricao_cliente,
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
                        "descricao": (
                            cliente.endereco.descricao if cliente.endereco else None
                        ),
                        "ultima_venda": {
                            "descricao": (
                                ultima_venda.descricao if ultima_venda else None
                            ),
                            "data_venda": (
                                ultima_venda.data_venda.isoformat()
                                if ultima_venda
                                else None
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
        clientes = Cliente.objects.filter(empresa_id=empresa_id).select_related(
            "endereco"
        )
        # Construa a lista de dicionários contendo os dados de cada cliente
        clientes_data = []
        for cliente in clientes:
            data = {
                "id_cliente": str(cliente.id_cliente),
                "nome": cliente.nome_cliente,
                "telefone": cliente.telefone_cliente,
                "descricao": cliente.descricao_cliente,
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
