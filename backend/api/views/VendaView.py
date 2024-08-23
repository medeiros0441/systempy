from api.permissions import permissions, CustomPermission
from api.user import UserInfo
from django.db.models import Q
from ..processos.venda import processos
from django.http import JsonResponse
import json
from api.models import (
    Usuario,
    ItemCompra,
    Produto,
    Venda,
    Loja,
    Cliente,
    Associado,
    GestaoGalao,
)
from .PdvView import PdvView, Transacao_pdvView
from .PersonalizacaoView import PersonalizacaoView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VendaView(APIView):
    permission_classes = [CustomPermission(codigo_model=7, auth_required=True)]

    def get(self, request):
        try:
            id_empresa = UserInfo.get_id_empresa(request, True)
            id_usuario = UserInfo.get_id_usuario(request)
            context = {}
            associacao = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

            produtos = Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas),
                loja__empresa_id=id_empresa,
                status=True,
            )
            lojas = Loja.objects.filter(Q(id_loja__in=ids_lojas_associadas))

            vendas = Venda.objects.filter(
                Q(loja_id__in=ids_lojas_associadas),
                loja__empresa__id_empresa=id_empresa,
            ).prefetch_related("loja")
            context = {
                "success": True,
                "lojas": list(lojas.values()),
                "produtos": list(produtos.values()),
                "vendas": list(vendas.values()),
            }

            return Response(context, status=status.HTTP_200_OK)
        except Associado.DoesNotExist:
            return Response(
                {
                    "message": "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Produto.DoesNotExist:
            return Response(
                {
                    "message": "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            id = UserInfo.get_id_usuario(request)
            dados = json.loads(request.body.decode("utf-8"))
            data, mensagem_erro = self._validar_dados_formulario(dados, id)
            if data is None:
                return Response(
                    {"error": mensagem_erro}, status=status.HTTP_400_BAD_REQUEST
                )

            venda, mensagem = processos.criar_ou_atualizar_venda(data)
            if venda is not None:
                if venda.metodo_entrega == "entrega no local":
                    id_motoboy = dados.get("motoboy", "").strip()
                    if id_motoboy != "0":
                        processos.processo_entrega(venda=venda, id_motoboy=id_motoboy)

                # Processando transação
                Transacao_pdvView.processar_trasacao_pdv(venda, request)

                # Processa o carrinho
                carrinho = dados.get("carrinho")
                processos._processar_carrinho(carrinho, venda)

                # Processa os dados dos galões
                galoes_troca = dados.get("galoes_troca")
                processos._processar_dados_galoes(galoes_troca, venda)

                return Response(
                    {"success": True, "message": mensagem}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": mensagem_erro}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _validar_dados_formulario(self, data_formulario, id):
        dados = {}

        try:
            desconto = processos.converter_para_decimal(
                data_formulario.get("desconto", None)
            )
            metodo_entrega = data_formulario.get("metodo_entrega", "").strip()
            taxa_entrega = data_formulario.get("taxa_entrega", "").strip()

            if metodo_entrega != "0":
                if metodo_entrega == "entrega no local":
                    taxa_entrega_decimal = processos.converter_para_decimal(
                        taxa_entrega
                    )
                    if taxa_entrega_decimal is None or taxa_entrega_decimal <= 0:
                        return None, "Taxa de entrega inválida."

            valor_pago = processos.converter_para_decimal(
                data_formulario.get("valor_pago", "").strip()
            )
            total_apagar = processos.converter_para_decimal(
                data_formulario.get("total_apagar", "").strip()
            )
            troco = processos.converter_para_decimal(data_formulario.get("troco", 0.0))

            forma_pagamento_str = data_formulario.get("forma_pagamento")
            estado_transacao = data_formulario.get("estado_transacao")

            if estado_transacao == "0" or forma_pagamento_str == "0":
                return None, "Estado da transação ou forma de pagamento inválidos."

            forma_pagamento_int = self._verificar_forma_pagamento(forma_pagamento_str)

            if forma_pagamento_int is None:
                return None, "Forma de pagamento inválida."

            if forma_pagamento_int == 1:
                if (
                    valor_pago is None
                    or total_apagar is None
                    or valor_pago <= 0.0
                    or valor_pago < total_apagar
                ):
                    return None, "Valor pago é inválido."
            else:
                valor_pago = total_apagar

            id_loja = data_formulario.get("loja")
            if id_loja == "0":
                id_loja = PersonalizacaoView.get_loja_id(id)
                if id_loja is None:
                    return None, "Loja não está selecionada."
            dados["loja"] = Loja.objects.get(id_loja=id_loja)

            id_cliente = data_formulario.get("id_cliente")
            if id_cliente != "0":
                dados["cliente"] = Cliente.objects.get(id_cliente=id_cliente)
            else:
                dados["cliente"] = None

            dados.update(
                {
                    "forma_pagamento": forma_pagamento_str,
                    "tipo_pagamento": forma_pagamento_int,
                    "estado_transacao": estado_transacao,
                    "desconto": desconto,
                    "metodo_entrega": metodo_entrega,
                    "taxa_entrega": taxa_entrega,
                    "valor_pago": valor_pago,
                    "troco": troco,
                    "valor_total": total_apagar,
                    "user": Usuario.objects.get(id_usuario=id),
                    "desc_venda": data_formulario.get("descricao_venda"),
                    "id_venda": data_formulario.get("id_venda", None) or None,
                }
            )

            return dados, None
        except Exception as e:
            return None, f"Erro ao validar dados do formulário: {e}"

    def _verificar_forma_pagamento(self, forma_pagamento_str):
        FORMA_PAGAMENTO_MAP = {
            "dinheiro": 1,
            "cartao credito": 2,
            "cartao debito": 3,
            "pix": 4,
            "fiado": 5,
            "boleto": 6,
        }
        return FORMA_PAGAMENTO_MAP.get(forma_pagamento_str)

    def _open_venda(request):
        try:
            id_usuario = UserInfo.get_id_usuario(request)
            id_empresa = UserInfo.get_id_empresa(request)

            associacao = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            if not associacao.exists():
                raise Associado.DoesNotExist

            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)
            produtos = Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas),
                loja__empresa_id=id_empresa,
                status=True,
            )
            if not produtos.exists():
                raise Produto.DoesNotExist

            context = {
                "list_produtos": produtos,
                "open_modal": True,
            }
            return JsonResponse(context)

        except Associado.DoesNotExist:
            set_mensagem = (
                "Tivemos um problema para recuperar informações sobre Associado. "
                "Entre em contato com um administrador da assinatura. "
                "Você precisa estar associado a uma loja para realizar uma venda."
            )
            return JsonResponse(
                {"message": set_mensagem, "open_modal": False}, status=404
            )

        except Produto.DoesNotExist:
            set_mensagem = (
                "Tivemos um problema para recuperar os Produtos. "
                "Entre em contato com um administrador da assinatura. "
                "Você precisa ter produtos para vendê-los."
            )
            return JsonResponse(
                {"message": set_mensagem, "open_modal": False}, status=404
            )

        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse(
                {"message": mensagem_erro, "open_modal": False}, status=500
            )

    def GetProdutosVenda(self, request, id_venda):
        try:
            itens_compra = ItemCompra.objects.filter(venda_id=id_venda)
            detalhes_produtos = []

            for item in itens_compra:
                detalhes_produto = {
                    "idProduto": item.produto.id_produto,
                    "nome": item.produto.nome,
                    "precoVenda": item.produto.preco_venda,
                    "quantidade": item.quantidade,
                    "quantidadeAtualEstoque": item.produto.quantidade_atual_estoque,
                    "fabricante": item.produto.fabricante,
                    "descricao": item.produto.descricao,
                }
                detalhes_produtos.append(detalhes_produto)

            return Response(
                {
                    "success": True,
                    "message": "Venda processada.",
                    "listProdutos": detalhes_produtos,
                },
                status=status.HTTP_200_OK,
            )
        except Venda.DoesNotExist:
            return Response(
                {"message": "Venda não encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def GetRetornaveisVenda(self, request, id_venda):
        try:
            gestao_galoes = GestaoGalao.objects.filter(venda__id_venda=id_venda)
            data_list = []

            for gestao_galao in gestao_galoes:
                obj = {}
                if gestao_galao.galao_entrando:
                    galao = gestao_galao.galao_entrando
                    obj.update(
                        {
                            "validadeEntrada": galao.data_validade,
                            "fabricacaoEntrada": galao.data_fabricacao,
                            "tipoEntrada": galao.titulo,
                        }
                    )

                if gestao_galao.galao_saiu:
                    galao = gestao_galao.galao_saiu
                    obj.update(
                        {
                            "validadeSaida": galao.data_validade,
                            "fabricacaoSaida": galao.data_fabricacao,
                            "tipoSaida": galao.titulo,
                        }
                    )

                obj["descricaoGestao"] = gestao_galao.descricao
                data_list.append(obj)

            return Response(
                {
                    "success": True,
                    "message": "Venda processada.",
                    "listRetornaveis": data_list,
                },
                status=status.HTTP_200_OK,
            )
        except Venda.DoesNotExist:
            return Response(
                {"message": "Venda não encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def GetClienteVenda(self, request, id_venda):
        try:
            venda = Venda.objects.select_related("cliente", "cliente__endereco").get(
                id_venda=id_venda
            )
            cliente = venda.cliente

            if cliente:
                data = {
                    "idCliente": cliente.id_cliente,
                    "nome": cliente.nome,
                    "telefone": cliente.telefone,
                    "descricao": cliente.descricao,
                    "tipoCliente": cliente.tipo_cliente,
                    "rua": cliente.endereco.rua if cliente.endereco else None,
                    "numero": cliente.endereco.numero if cliente.endereco else None,
                    "cep": cliente.endereco.codigo_postal if cliente.endereco else None,
                    "estado": cliente.endereco.estado if cliente.endereco else None,
                    "bairro": cliente.endereco.bairro if cliente.endereco else None,
                    "cidade": cliente.endereco.cidade if cliente.endereco else None,
                    "descricaoEndereco": (
                        cliente.endereco.descricao if cliente.endereco else None
                    ),
                }
                return Response(
                    {"success": True, "message": "Venda processada.", "cliente": data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "success": False,
                    "message": "Não há cliente associado a essa venda",
                    "cliente": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Venda.DoesNotExist:
            return Response(
                {"message": "Venda não encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        except Cliente.DoesNotExist:
            return Response(
                {"message": "Cliente não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
