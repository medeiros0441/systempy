from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..def_global import erro, criar_alerta_js,verificar_permissoes
from ..static import Alerta, UserInfo
from ..models import (
    Venda,
    Configuracao,
    Usuario,
    Associado,
    Loja,
    Cliente,
    Produto,
    ItemCompra,
    Compra,
    GestaoGalao,
    Galao,
)
from ..forms import VendaForm, ClienteForm, EnderecoForm
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date
from django.utils import timezone
 
class views_venda:

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def lista_vendas(request, context=None, id_loja=None):

        id_empresa = UserInfo.get_id_empresa(request, True)
        if context is None:
            context = {}
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = criar_alerta_js(alerta)

        try:
            if id_loja is None:
                vendas = Venda.objects.filter(loja__empresa__id_empresa=id_empresa)
            else:
                vendas = Venda.objects.filter(
                    loja__empresa__id_empresa=id_empresa, loja_id_loja=id_loja
                )
            context["vendas"] = vendas
        except Venda.DoesNotExist:
            pass
        return render(request, "venda/lista_vendas.html", context)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def criar_venda(request):
        try:
            if request.method == "POST":
                return views_venda._insert_venda(request)
            else:
                return views_venda._open_venda(request)
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    def _insert_venda(request):
        try:

            for item_carrinho in request.POST.getlist("item_carrinho"):
                id_produto, quantidade = item_carrinho.split("|")
                produto = Produto.objects.filter(id_produto=id_produto)
                ItemCompra.produto = produto
                ItemCompra.quantidade = quantidade

            id_usuario = UserInfo.get_id_usuario(request)

            id_cliente = request.POST.get("id_cliente")
            if id_cliente != "0":
                form_cliente = ClienteForm(request.POST)
            
            loja = request.POST.get("loja")
            metodo_entrega = request.POST.get("metodo_entrega")
            valor_pago = request.POST.get("valor_pago")
            forma_pagamento = request.POST.get("forma_pagamento")
            estado_transacao = request.POST.get("estado_transacao")
            descricao = request.POST.get("descricao") 
            motoboy = request.POST.get("motoboy")  
            

            if (
                form_venda.is_valid()
                and form_cliente.is_valid()
                and form_endereco.is_valid()
            ):
                # Recuperar os dados dos formulários
                dados_venda = form_venda.cleaned_data
                dados_cliente = form_cliente.cleaned_data
                dados_endereco = form_endereco.cleaned_data
                # Aqui você pode criar instâncias dos modelos correspondentes e salvar no banco de dados
                venda = form_venda.save(
                    commit=False
                )  # Se precisar de lógica adicional antes de salvar
                cliente = form_cliente.save(commit=False)
                endereco = form_endereco.save(commit=False)
                venda.cliente = cliente
                venda.endereco = endereco
                venda.save()

                views_venda._processar_dados_galoes(request, venda)

            else:
                form_venda = VendaForm()
                form_cliente = ClienteForm()
                form_endereco = EnderecoForm()
            return ""
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    def _open_venda(request):
        try:
            context = {}
            id_usuario = UserInfo.get_id_usuario(request)
            id_empresa = UserInfo.get_id_empresa(request)

            associacao = Associado.objects.filter(
                usuario_id=id_usuario, status_acesso=True
            )
            # Obter os clientes da empresa
            clientes = Cliente.objects.filter(empresa_id=id_empresa)

            # Obtém uma lista de IDs de loja associadas
            ids_lojas_associadas = associacao.values_list("loja_id", flat=True)

            # Filtra os produtos com base nas lojas associadas
            produtos = Produto.objects.filter(
                Q(loja_id__in=ids_lojas_associadas), loja__empresa_id=id_empresa
            )

            # Inicializar os formulários
            form_venda = VendaForm(id_usuario)
            form_cliente = ClienteForm()
            form_endereco = EnderecoForm()
            # Criar o contexto
            context = {
                "list_clientes": clientes,
                "form_cliente": form_cliente,
                "form_venda": form_venda,
                "form_endereco": form_endereco,
                "list_produtos": produtos,
                "open_modal": True,
            }
            return views_venda.lista_vendas(request, context)
        except Associado.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar as lojas. Entre em contato com um administrador da assinatura. Você precisa estar associado a uma loja para realizar uma venda."
            )
            context["open_modal"] = False
            return views_venda.lista_vendas(request, context)
        except Produto.DoesNotExist:
            Alerta.set_mensagem(
                "Tivemos um problema para recuperar os Produtos. Entre em contato com um administrador da assinatura. Você precisa Ter produto para vender-los."
            )
            context["open_modal"] = False
            return views_venda.lista_vendas(request, context)
        except Exception as e:
            mensagem_erro = str(e)
            return erro(request, mensagem_erro)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def editar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def selecionar_venda(request, venda_id):

        return views_venda.lista_vendas(request)

    @staticmethod
    @verificar_permissoes(codigo_model=7)
    def excluir_venda(request, venda_id):
        if (
            request.session.get("id_empresa", 0) != 0
            and request.session.get("id_usuario", 0) != 0
            and request.session.get("status_acesso", "") == "ativo"
        ):
            # Lógica para excluir a venda com id=venda_id
            return HttpResponse(f"Excluindo a venda {venda_id}")
        else:
            return erro(request, "Você não está autorizado a fazer esta requisição.")

    def _processar_dados_galoes(request, venda, cliente):
        if request.method == "POST":
            data_galao_entrada = data_fabricacao_entrada = tipo_entrada = (
                data_galao_saida
            ) = data_fabricacao_saida = tipo_saida = descricao = None

            for chave, valor in request.POST.items():
                if chave.startswith("data_validade_entrada_"):
                    data_galao_entrada = datetime.strptime(valor, "%m/%Y").date()
                elif chave.startswith("data_fabricacao_entrada_"):
                    data_fabricacao_entrada = datetime.strptime(valor, "%m/%Y").date()
                elif chave.startswith("tipo_entrada_"):
                    tipo_entrada = valor
                elif chave.startswith("data_validade_saida_"):
                    data_galao_saida = datetime.strptime(valor, "%m/%Y").date()
                elif chave.startswith("data_fabricacao_saida_"):
                    data_fabricacao_saida = datetime.strptime(valor, "%m/%Y").date()
                elif chave.startswith("tipo_saida_"):
                    tipo_saida = valor
                elif chave.startswith("id_descricao_gestão_galao"):
                    descricao = valor

            galao_entrada, created_entrada = Galao.objects.get_or_create(
                data_validade=parse_date(data_galao_entrada),
                titulo=tipo_entrada,
                loja=venda.loja,
            )
            galao_saida, created_saida = Galao.objects.get_or_create(
                data_validade=parse_date(data_galao_saida),
                titulo=tipo_saida,
                loja=venda.loja,
            )

            # Atualizar as quantidades
            if created_entrada:
                galao_entrada.quantidade = 1
            else:
                galao_entrada.quantidade += 1

            galao_entrada.update = timezone.now()
            galao_entrada.save()

            if created_saida:
                galao_saida.quantidade = -1
            else:
                galao_saida.quantidade -= 1
            galao_saida.update = timezone.now()
            galao_saida.save()

            # Criar um objeto GestaoGalao
            gestao_galao = GestaoGalao()
            gestao_galao.descricao = descricao
            gestao_galao.galao_entrando = galao_entrada
            gestao_galao.galao_saiu = galao_saida
            gestao_galao.venda = venda
            gestao_galao.cliente = cliente
            gestao_galao.update = timezone.now()
            gestao_galao.save()
