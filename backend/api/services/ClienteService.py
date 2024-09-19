from api.serializers import ClienteSerializer, EnderecoSerializer
from api.models import ClienteModel, VendaModel, EnderecoModel, ItemCompraModel
from api.utils import Utils
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import  get_object_or_404
from django.db.models import F

class ClienteService:
    @staticmethod
    def create_cliente(cliente_data):
        try:
            cliente_serializer = ClienteSerializer(data=cliente_data)
            if cliente_serializer.is_valid():
                cliente = cliente_serializer.save()
                return cliente, True, "Cliente criado com sucesso."
            else:
                # Retorna erros de validação como uma string para facilitar o tratamento
                error_messages = ', '.join([f"{k}: {', '.join(v)}" for k, v in cliente_serializer.errors.items()])
                return None, False, f"Erro de validação: {error_messages}"
        except Exception as e:
            return None, False, str(e)

    @staticmethod 
    def update_cliente(cliente_id, cliente_data):
        try:
            cliente = ClienteModel.objects.get(pk=cliente_id)
            if cliente_data.get('ultima_compra') == '':
                cliente_data['ultima_compra'] = None
            cliente_serializer = ClienteSerializer(cliente, data=cliente_data, partial=True)
            if cliente_serializer.is_valid():
                cliente = cliente_serializer.save()
                return cliente, True, "Cliente atualizado com sucesso."

            error_messages = []
            for field, errors in cliente_serializer.errors.items():
                error_messages.append(f"{field}: {'; '.join(errors)}")
            error_message = " | ".join(error_messages)
            return None, False, error_message

        except ClienteModel.DoesNotExist:
            return None, False, "Cliente não encontrado."

        except Exception as e:
            return None, False, f"Erro ao atualizar cliente: {str(e)}"


    @staticmethod
    def delete_cliente(cliente_id, empresa_id):
        try:
            cliente = ClienteModel.objects.get(id_cliente=cliente_id, empresa_id=empresa_id)

            if cliente:
                cliente.delete()
                return True, "Cliente excluído com sucesso"
            else:
                return False, "Cliente não encontrado"

        except ClienteModel.DoesNotExist:
            return False, "Cliente não encontrado"

        except Exception as e:
            return False, f"Erro ao excluir cliente: {str(e)}"


    
    @staticmethod
    def get_clientes_by_empresa(empresa_id):
        try:
            clientes = ClienteModel.objects.filter(empresa_id=empresa_id)

            if not clientes.exists():
                return None   

            serializer = ClienteSerializer(clientes, many=True)
            return serializer.data  

        except Exception as e:
            return None   

    @staticmethod
    def get_cliente(id_cliente):
        try:
            cliente = get_object_or_404(ClienteModel.objects.select_related("endereco"), id_cliente=id_cliente)
            cliente_data = ClienteSerializer(cliente).data
            return {"success": True, "data": cliente_data}
        except Exception as e:
            return {"success": False, "message": f"Ocorreu um erro ao processar a solicitação: {e}", "status": 500}

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