from api.serializers import ClienteSerializer, EnderecoSerializer
from api.models import ClienteModel, VendaModel, EnderecoModel, ItemCompraModel
from api.utils import Utils
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import  get_object_or_404
from django.db.models import F

class ClienteService:
    @staticmethod
    def create_cliente(cliente_data, endereco_id):
        try:
            cliente_data["endereco_id"] = endereco_id
            cliente_serializer = ClienteSerializer(data=cliente_data)
            if cliente_serializer.is_valid():
                cliente = cliente_serializer.save()
                return cliente, True, "Cliente criado com sucesso."
            return None, False, cliente_serializer.errors
        except Exception as e:
            return None, False, str(e)

    @staticmethod
    def update_cliente(cliente_id, cliente_data):
        try:
            cliente = ClienteModel.objects.get(pk=cliente_id)
            cliente_serializer = ClienteSerializer(cliente, data=cliente_data, partial=True)
            if cliente_serializer.is_valid():
                cliente = cliente_serializer.save()
                return cliente, True, "Cliente atualizado com sucesso."
            return None, False, cliente_serializer.errors
        except ClienteModel.DoesNotExist:
            return None, False, "Cliente não encontrado."
        except Exception as e:
            return None, False, str(e)

    @staticmethod
    def get_cliente(cliente_id):
        cliente = get_object_or_404(ClienteModel, pk=cliente_id)
        return Utils.modelo_para_json(cliente)

    @staticmethod
    def delete_cliente(cliente_id, empresa_id):
        try:
            cliente = ClienteModel.objects.get(id_cliente=cliente_id, empresa_id=empresa_id)

            if cliente:
                cliente.delete()
                return {"success": True, "message": "Cliente excluído com sucesso"}
            else:
                return {"error": "Cliente não encontrado"}, 404

        except ClienteModel.DoesNotExist:
            return {"error": "Cliente não encontrado"}, 404

        except Exception as e:
            return {"error": str(e)}, 500

    
    @staticmethod
    def get_clientes_by_empresa(empresa_id):
        try:
            clientes = ClienteModel.objects.filter(empresa_id=empresa_id)

            if not clientes.exists():
                return {"message": "Não foram encontrados clientes para esta empresa."}, 404

            clientes_data = []
            for cliente in clientes:
                try:
                    ultima_venda = VendaModel.objects.filter(cliente=cliente).order_by("-insert").first()
                    endereco = EnderecoModel.objects.filter(id_endereco=cliente.endereco_id).first()
                    cliente_data = Utils.modelo_para_json(cliente, endereco)
                    cliente_data.update({
                        "ultima_venda": {
                            "descricao": ultima_venda.descricao if ultima_venda else None,
                            "data_venda": ultima_venda.data_venda if ultima_venda else None,
                            "forma_pagamento": ultima_venda.forma_pagamento if ultima_venda else None,
                            "valor_total": str(ultima_venda.valor_total) if ultima_venda else None,
                            "produtos": [item.produto.nome for item in ultima_venda.itemcompra_set.all()] if ultima_venda else None,
                        },
                    })
                    clientes_data.append(cliente_data)
                except Exception as e:
                    print(f"Erro ao processar cliente {cliente.id_cliente}: {e}")

            return {"success": True, "data": clientes_data}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_cliente(empresa_id):
        try:
            clientes = ClienteModel.objects.filter(empresa_id=empresa_id).select_related("endereco")

            if not clientes:
                return {"message": "Não foram encontrados clientes para esta empresa."}, 404

            clientes_data = [Utils.modelo_para_json(cliente) for cliente in clientes]
            return {"data": clientes_data, "success": True}, 200
        except Exception as e:
            return {"message": f"Ocorreu um erro ao processar a solicitação: {e}"}, 500

    @staticmethod
    def get_vendas_by_cliente(id_cliente):
        try:
            vendas = VendaModel.objects.filter(cliente_id=id_cliente).order_by("-insert")
            vendas_data = []

            for venda in vendas:
                itens_compra = ItemCompraModel.objects.filter(venda=venda)
                itens_data = list(itens_compra.values(
                    "id_item_compra", "quantidade", "insert", "update", nome=F("produto__nome")
                ))

                venda_data = Utils.modelo_para_json(venda)
                venda_data.update({
                    "itens_compra": itens_data,
                    "usuario": venda.usuario.nome_completo,
                    "loja": venda.loja.nome,
                    "cliente_id": venda.cliente_id,
                })

                vendas_data.append(venda_data)

            return {"data": vendas_data, "success": True}, 200

        except ObjectDoesNotExist:
            return {"error": "Cliente não encontrado.", "success": False}, 404
        except ValidationError as e:
            return {"error": str(e), "success": False}, 400
        except Exception as e:
            return {"error": "Erro interno no servidor.", "success": False, "details": str(e)}, 500