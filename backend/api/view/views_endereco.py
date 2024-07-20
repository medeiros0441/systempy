from django.shortcuts import render, get_object_or_404, redirect
from ..models import Endereco, Configuracao
from api.utils import Utils
from api.static import Alerta, UserInfo
from django.db import IntegrityError
from api import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


class views_endereco:

    @staticmethod
    @Utils.verificar_permissoes(3, True)
    def lista_enderecos(request, context=None):
        if context is None:
            context = {}

        enderecos = Endereco.objects.all()
        context["enderecos"] = enderecos
        alerta = Alerta.get_mensagem()
        if alerta:
            context["alerta_js"] = Utils.criar_alerta_js(alerta)

        return render(request, "endereco/lista_enderecos.html", context)

    @staticmethod
    @Utils.verificar_permissoes(3, True)
    def criar_endereco(request):
        if request.method == "POST":
            form = {}
            if form.is_valid():
                form.save()
                Alerta.set_mensagem("Cadastrado com Sucesso.")
                return redirect("lista_enderecos")

            else:
                return views_endereco.lista_enderecos(
                    request, {"open_modal": True, "form": form}
                )
        else:
            form = {}
            return views_endereco.lista_enderecos(
                request, {"open_modal": True, "form": form}
            )

    @staticmethod
    @Utils.verificar_permissoes(3, True)
    def selecionar_endereco(request, pk):
        endereco = get_object_or_404(Endereco, pk=pk)
        return views_endereco.lista_enderecos(
            request, {"open_modal": True, "endereco": endereco}
        )

    @staticmethod
    @Utils.verificar_permissoes(3, True)
    def editar_endereco(request, pk):
        endereco = get_object_or_404(Endereco, pk=pk)
        if request.method == "POST":
            form = {}
            if form.is_valid():
                form.save()
                Alerta.set_mensagem("Endereço Editado")
                return redirect("lista_enderecos")

        else:
            form = {}
            return views_endereco.lista_enderecos(
                request, {"open_modal": True, "form": form}
            )

    @staticmethod
    @Utils.verificar_permissoes(3, True)
    def delete_endereco(request, pk):
        try:
            endereco = get_object_or_404(Endereco, pk=pk)
            endereco.delete()
            Alerta.set_mensagem("Endereço excluído com sucesso.")
        except IntegrityError as e:
            # Captura o erro de integridade e fornece uma mensagem adequada
            Alerta.set_mensagem(
                "Não é possível excluir este endereço. Está sendo usado em outro lugar."
            )
        return redirect("lista_enderecos")

    @staticmethod
    @csrf_exempt
    @Utils.verificar_permissoes(8, True)
    def api_create_endereco(request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                endereco, status, msg = views_endereco.create_endereco_data(data)
                if status:
                    response_data = Utils.modelo_para_json(endereco)
                    return JsonResponse(
                        {"success": status, "data": response_data, "message": msg}
                    )
                else:
                    return JsonResponse({"success": status, "message": msg}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Método não permitido"}, status=405)

    @staticmethod
    @Utils.verificar_permissoes(8, True)
    @csrf_exempt
    def api_update_endereco(request, endereco_id):
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                endereco, status, msg = views_endereco.update_endereco_data(
                    endereco_id, data
                )
                if status:
                    return JsonResponse(
                        {
                            "success": status,
                            "data": Utils.modelo_para_json(endereco),
                            "message": msg,
                        }
                    )
                else:
                    return JsonResponse({"success": status, "message": msg}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "Método não permitido"}, status=405)

    def create_endereco_data(data):
        """
        Cria uma instância do modelo Endereco com base nos dados fornecidos.
        """
        try:
            endereco = models.Endereco.objects.create(
                rua=data.get("rua", ""),
                numero=data.get("numero", ""),
                bairro=data.get("bairro", ""),
                cidade=data.get("cidade", ""),
                estado=data.get("estado", ""),
                codigo_postal=data.get("codigo_postal", ""),
                descricao=data.get("descricao", ""),
                insert=Utils.obter_data_hora_atual(),
                update=Utils.obter_data_hora_atual(),
            )
            return endereco, True, "Cadastro de endereço efetuado com sucesso."
        except Exception as e:
            return None, False, f"Erro ao cadastrar endereço: {str(e)}"

    def update_endereco_data(endereco_id, data):
        """
        Atualiza uma instância existente do modelo Endereco com base nos dados fornecidos.
        """
        try:
            endereco = models.Endereco.objects.get(id_endereco=endereco_id)
            endereco.rua = data.get("rua", endereco.rua)
            endereco.numero = data.get("numero", endereco.numero)
            endereco.bairro = data.get("bairro", endereco.bairro)
            endereco.cidade = data.get("cidade", endereco.cidade)
            endereco.estado = data.get("estado", endereco.estado)
            endereco.codigo_postal = data.get("codigo_postal", endereco.codigo_postal)
            endereco.descricao = data.get("descricao", endereco.descricao)
            endereco.update = Utils.obter_data_hora_atual()
            endereco.save()
            return endereco, True, "Atualização de endereço efetuada."
        except models.Endereco.DoesNotExist:
            return None, False, f"Endereço com ID {endereco_id} não encontrado."
        except Exception as e:
            return None, False, f"Erro ao atualizar endereço: {str(e)}"
