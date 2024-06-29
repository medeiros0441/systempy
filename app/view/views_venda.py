from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from app.utils import Utils
from app.static import Alerta, UserInfo
from django.db.models import Q
from ..processos.venda import processos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app import models
from .views_erro import views_erro
from .views_pdv import views_pdv, views_transacao_pdv
from .views_pdv import views_associado_pdv, views_registro_diario_pdv
from .views_personalizacao import views_personalizacao


class views_venda:

    @staticmethod
    @Utils.verificar_permissoes(7, True)
    def lista_vendas(request, context={}, id_loja=None, **kwargs):

        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = Utils.criar_alerta_js(alerta)

        return render(request, "venda/lista_vendas.html", context)

    @staticmethod
    @Utils.verificar_permissoes(7, True)
    def editar_venda(request, id_venda):
        try:
            context = {}
            alerta = Alerta.get_mensagem()
            if alerta:
                context["alerta_js"] = Utils.criar_alerta_js(alerta)
            context["type"] = 2
            context["id_venda"] = id_venda

            return render(request, "venda/formulario_venda.html", context)
        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)

    @staticmethod
    @Utils.verificar_permissoes(7, True)
    def criar_venda(request, context={}):
        try:
            alerta = Alerta.get_mensagem()
            if alerta:
                context["alerta_js"] = Utils.criar_alerta_js(alerta)
            context["type"] = 1
            return render(request, "venda/formulario_venda.html", context)
        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)

    @csrf_exempt
    def obter_dados(request):
        if request.method == "GET":
            try:
                id_empresa = UserInfo.get_id_empresa(request, True)
                id_usuario = UserInfo.get_id_usuario(request)
                context = {}
                associacao = models.Associado.objects.filter(
                    usuario_id=id_usuario, status_acesso=True
                )
                ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

                produtos = models.Produto.objects.filter(
                    Q(loja_id__in=ids_lojas_associadas),
                    loja__empresa_id=id_empresa,
                    status=True,
                )
                lojas = models.Loja.objects.filter(Q(id_loja__in=ids_lojas_associadas))

                vendas = models.Venda.objects.filter(
                    Q(loja_id__in=ids_lojas_associadas),
                    loja__empresa__id_empresa=id_empresa,
                ).prefetch_related("loja")
                context = {
                    "success": True,
                    "lojas": list(lojas.values()),
                    "produtos": list(produtos.values()),
                    "vendas": list(vendas.values()),
                }

                return JsonResponse(context)
            except models.Associado.DoesNotExist:
                context["menssage"] = (
                    "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
                )
            except models.Produto.DoesNotExist:
                context["menssage"] = (
                    "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
                )
        return JsonResponse(
            {
                "error": "erro, ao buscar dados..",
            },
            context,
            status=405,
        )

    @Utils.verificar_permissoes(7, True)
    @csrf_exempt
    def processar_venda(request):
        try:
            if request.method == "POST":
                # Processa a venda
                id = UserInfo.get_id_usuario(request)
                dados = json.loads(request.body.decode("utf-8"))
                data, mensagem_erro = views_venda.validar_dados_formulario(dados, id)
                venda, menssagem = processos.criar_ou_atualizar_venda(data)
                if venda is not None:

                    if venda.metodo_entrega == "entrega no local":
                        id_motoboy = dados.get("motoboy", "").strip()
                        if id_motoboy != "0":
                            processos.processo_entrega(
                                venda=venda, id_motoboy=id_motoboy
                            )
                    ##processando transacao
                    views_transacao_pdv.processar_trasacao_pdv(venda, request)
                    # Processa o carrinho
                    carrinho = dados.get("carrinho")
                    processos._processar_carrinho(carrinho, venda)
                    # Processa os dados dos galões
                    galoes_troca = dados.get("galoes_troca")
                    processos._processar_dados_galoes(galoes_troca, venda)
                    return JsonResponse({"success": True, "message": menssagem})
                elif mensagem_erro:
                    return JsonResponse({"error": mensagem_erro})

        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"error": mensagem_erro}, status=500)

    def validar_dados_formulario(data_formulario, id):
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

            forma_pagamento_int = views_venda.verificar_forma_pagamento(
                forma_pagamento_str
            )

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
                id_loja = views_personalizacao.get_loja_id(id)
                if id_loja is None:
                    return None, "Loja não está selecionada."
            dados["loja"] = models.Loja.objects.get(id_loja=id_loja)

            id_cliente = data_formulario.get("id_cliente")
            if id_cliente != "0":
                dados["cliente"] = models.Cliente.objects.get(id_cliente=id_cliente)
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
                    "user": models.Usuario.objects.get(id_usuario=id),
                    "desc_venda": data_formulario.get("descricao_venda"),
                    "id_venda": data_formulario.get("id_venda", None) or None,
                }
            )

            return dados, None
        except Exception as e:
            return None, f"Erro ao validar dados do formulário: {e}"

    def verificar_forma_pagamento(forma_pagamento_str):
        FORMA_PAGAMENTO_MAP = {
            "dinheiro": 1,
            "cartao credito": 2,
            "cartao debito": 3,
            "pix": 4,
            "fiado": 5,
            "boleto": 6,
        }
        return FORMA_PAGAMENTO_MAP.get(forma_pagamento_str)

    @staticmethod
    @Utils.verificar_permissoes(7, True)
    def _open_venda(request):
        try:
            context = {}
            id_usuario = UserInfo.get_id_usuario(request)
            id_empresa = UserInfo.get_id_empresa(request)

            associacao = models.Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            # Obtém uma lista de IDs de loja associadas
            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

            # Filtra os produtos com base nas lojas associadas
            produtos = models.Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas),
                loja__empresa_id=id_empresa,
                status=True,
            )
            context = {
                "list_produtos": produtos,
                "open_modal": True,
            }
            return views_venda.lista_vendas(request, context)
        except models.Associado.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
            )
            context["open_modal"] = False
            return views_venda.lista_vendas(request, context)
        except models.Produto.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
            )
            context["open_modal"] = False
            return views_venda.lista_vendas(request, context)
        except Exception as e:
            mensagem_erro = str(e)
            return views_erro.erro(request, mensagem_erro)

    @staticmethod
    @Utils.verificar_permissoes(7, True)
    def selecionar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @csrf_exempt
    def selecionar_produto_by_venda(request, id_venda):
        try:
            # Tenta encontrar a venda pelo ID
            itens_compra = models.ItemCompra.objects.filter(venda_id=id_venda)
            # Inicializa uma lista para armazenar os detalhes dos produtos
            detalhes_produtos = []
            # Itera sobre os itens de compra para obter os detalhes dos produtos
            for item in itens_compra:
                detalhes_produto = {
                    "id_produto": item.produto.id_produto,
                    "nome": item.produto.nome,
                    "preco_venda": item.produto.preco_venda,
                    "quantidade": item.quantidade,
                    "quantidade_atual_estoque": item.produto.quantidade_atual_estoque,
                    "fabricante": item.produto.fabricante,
                    "descricao": item.produto.descricao,
                    # Adicione mais campos do produto conforme necessário
                }
                detalhes_produtos.append(detalhes_produto)
            # Retorna os produtos como JSON
            return JsonResponse(
                {
                    "success": True,
                    "message": "Venda processada.",
                    "list_produtos": detalhes_produtos,
                }
            )
        except models.Venda.DoesNotExist:
            # Se a venda não for encontrada, retorna uma resposta de erro
            return JsonResponse({"message": "Venda não encontrada"}, status=404)
        except Exception as e:
            # Se ocorrer qualquer outro erro, retorna uma resposta de erro com a mensagem do erro
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @csrf_exempt
    def selecionar_retornaveis_by_venda(request, id_venda):
        try:
            gestao_galoes = models.GestaoGalao.objects.filter(venda__id_venda=id_venda)
            # Lista para armazenar os objetos obj
            data_list = []
            # Itera sobre os objetos GestaoGalao
            for gestao_galao in gestao_galoes:
                obj = {}

                # Verifica se é entrada ou saída e preenche as informações correspondentes
                if gestao_galao.galao_entrando:
                    galao = gestao_galao.galao_entrando
                    obj["validade_entrada"] = galao.data_validade
                    obj["fabricacao_entrada"] = galao.data_fabricacao
                    obj["tipo_entrada"] = galao.titulo

                if gestao_galao.galao_saiu:
                    galao = gestao_galao.galao_saiu
                    obj["validade_saida"] = galao.data_validade
                    obj["fabricacao_saida"] = galao.data_fabricacao
                    obj["tipo_saida"] = galao.titulo

                # Adiciona a descrição do GestaoGalao
                obj["descricao_gestao"] = gestao_galao.descricao

                data_list.append(obj)

            # Retorna os produtos como JSON
            return JsonResponse(
                {
                    "success": True,
                    "message": "Venda processada.",
                    "list_retornaveis": data_list,
                }
            )
        except models.Venda.DoesNotExist:
            # Se a venda não for encontrada, retorna uma resposta de erro
            return JsonResponse({"message": "Venda não encontrada"}, status=404)
        except Exception as e:
            # Se ocorrer qualquer outro erro, retorna uma resposta de erro com a mensagem do erro
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @csrf_exempt
    def selecionar_cliente_by_venda(request, id_venda):
        try:
            # Obtém a venda junto com o cliente e suas informações de endereço relacionadas
            venda = models.Venda.objects.select_related(
                "cliente", "cliente__endereco"
            ).get(id_venda=id_venda)

            # Agora você pode acessar o cliente e seu endereço diretamente sem fazer consultas adicionais
            cliente = venda.cliente
            if cliente:
                # Construir o dicionário de dados do cliente e sua última venda
                data = {
                    "id_cliente": cliente.id_cliente,
                    "nome": cliente.nome,
                    "telefone": cliente.telefone,
                    "descricao": cliente.descricao,
                    "tipo_cliente": cliente.tipo_cliente,
                    "rua": cliente.endereco.rua if cliente.endereco else None,
                    "numero": (cliente.endereco.numero if cliente.endereco else None),
                    "cep": (
                        cliente.endereco.codigo_postal if cliente.endereco else None
                    ),
                    "estado": (cliente.endereco.estado if cliente.endereco else None),
                    "bairro": (cliente.endereco.bairro if cliente.endereco else None),
                    "cidade": (cliente.endereco.cidade if cliente.endereco else None),
                    "descricao": (
                        cliente.endereco.descricao if cliente.endereco else None
                    ),
                }
                return JsonResponse(
                    {"success": True, "message": "Venda processada.", "cliente": data}
                )
            return JsonResponse(
                {
                    "success": False,
                    "message": "não há cliente associado a essa venda",
                    "cliente": None,
                }
            )

        except models.Venda.DoesNotExist:
            return JsonResponse({"message": "Venda não encontrada"}, status=404)

        except models.Cliente.DoesNotExist:
            return JsonResponse({"message": "cliente não encontrada"}, status=404)
        except Exception as e:
            mensagem_erro = str(e)
            return JsonResponse({"message": mensagem_erro}, status=500)

    @staticmethod
    @Utils.verificar_permissoes(7, True)
    def excluir_venda(request, venda_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para excluir a venda com id=venda_id
            return HttpResponse(f"Excluindo a venda {venda_id}")
        else:
            return views_erro.erro(
                request, "Você não está autorizado a fazer esta requisição."
            )
