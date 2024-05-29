from django.shortcuts import render, get_object_or_404, redirect
from app.utils import Utils
from app import models
from app.static import Alerta, UserInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import app.view as view


class views_caixa:
    @staticmethod
    @Utils.verificar_permissoes(codigo_model="pdv")
    def pdv(request):

        return render(request, "pdv/lista_PDV.html")

    def get_lista(self, request, id=None):
        id_empresa = UserInfo.get_id_empresa(request)

        if id:
            PDV = models.PDV.objects.get(id_caixa=id)
            data = {
                "id_caixa": PDV.id_caixa,
                "nome": PDV.nome,
                "loja": PDV.loja_id,
                "dia": PDV.dia,
                "insert": PDV.insert,
                "update": PDV.update,
                "saldo_inicial": PDV.saldo_inicial,
                "saldo_final": PDV.saldo_final,
            }
        else:
            PDVs = models.PDV.objects.get(loja__empresa_id=id_empresa)
            data = [
                {
                    "id_caixa": PDV.id_caixa,
                    "nome": PDV.usuario_nome,
                    "nome": PDV.nome,
                    "loja": PDV.loja.id,
                    "dia": PDV.dia,
                    "insert": PDV.insert,
                    "update": PDV.update,
                    "saldo_inicial": PDV.saldo_inicial,
                    "saldo_final": PDV.saldo_final,
                }
                for PDV in PDVs
            ]
        return JsonResponse(data, safe=False)

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        loja = models.Loja.objects.get(id=data["loja"])
        PDV = models.PDV.objects.create(
            nome=data["nome"],
            loja=loja,
            dia=data["dia"],
            saldo_inicial=data["saldo_inicial"],
            saldo_final=data.get("saldo_final", None),
        )
        return JsonResponse(
            {
                "id_caixa": PDV.id_caixa,
                "nome": PDV.nome,
                "loja": PDV.loja_id,
                "dia": PDV.dia,
                "insert": PDV.insert,
                "update": PDV.update,
                "saldo_inicial": PDV.saldo_inicial,
                "saldo_final": PDV.saldo_final,
            }
        )

    @csrf_exempt
    def put(self, request, id):
        data = json.loads(request.body)
        PDV = models.PDV.objects.get(id_caixa=id)
        PDV.nome = data["nome"]
        PDV.dia = data["dia"]
        PDV.saldo_inicial = data["saldo_inicial"]
        PDV.saldo_final = data.get("saldo_final", PDV.saldo_final)
        PDV.save()
        return JsonResponse(
            {
                "id_caixa": PDV.id_caixa,
                "nome": PDV.nome,
                "loja": PDV.loja.id,
                "dia": PDV.dia,
                "insert": PDV.insert,
                "update": PDV.update,
                "saldo_inicial": PDV.saldo_inicial,
                "saldo_final": PDV.saldo_final,
            }
        )

    @csrf_exempt
    def delete(self, request, id):
        PDV = models.PDV.objects.get(id_caixa=id)
        PDV.delete()
        return JsonResponse({"message": "Caixa deletada com sucesso!"})


class views_transacao:

    @staticmethod
    @Utils.verificar_permissoes(codigo_model="transacao")
    def lista_transacao(request):

        return render(request, "caixa/transacao/lista_transacao.html")
