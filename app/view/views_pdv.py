from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, DateTimeField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import app.view as view
from ..models import Usuario, PDV, Loja
from app.static import Alerta, UserInfo
from app.utils import Utils 
  
from django.core.exceptions import ObjectDoesNotExist

class views_pdv:
    @staticmethod
    @Utils.verificar_permissoes(codigo_model="pdv")
    def pdv(request):
        return render(request, "pdv/lista_pdv.html")
        
    def get_lista(request, id=None):
            id_empresa = UserInfo.get_id_empresa(request)
            data = []
            
            try:
                if id:
                    pdv_instance = PDV.objects.get(id_pdv=id)
                    data = {
                        "id_pdv": pdv_instance.id_pdv,
                        "nome": pdv_instance.nome,
                        "loja": pdv_instance.loja_id,
                        "dia": pdv_instance.dia,
                        "insert": pdv_instance.insert,
                        "update": pdv_instance.update,
                        "saldo_inicial": pdv_instance.saldo_inicial,
                        "saldo_final": pdv_instance.saldo_final,
                    }
                else:
                    pdvs = PDV.objects.filter(loja__empresa_id=id_empresa)
                    if pdvs.exists():
                        data = [
                            {
                                "id_pdv": pdv.id_pdv,
                                "nome": pdv.nome,
                                "loja": pdv.loja.id,
                                "dia": pdv.dia,
                                "insert": pdv.insert,
                                "update": pdv.update,
                                "saldo_inicial": pdv.saldo_inicial,
                                "saldo_final": pdv.saldo_final,
                            }
                            for pdv in pdvs
                        ]
                    else:
                        data = {"error": "Nenhum PDV encontrado para a empresa fornecida."}
                        
                return JsonResponse(data)
            except PDV.DoesNotExist:
                data = {"error": "PDV não encontrado."}
                return JsonResponse(data, status=404)
        
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        loja = Loja.objects.get(id=data["loja"])
        PDVs = PDV.objects.create(
            nome=data["nome"],
            loja=loja,
            dia=data["dia"],
            saldo_inicial=data["saldo_inicial"],
            saldo_final=data.get("saldo_final", None),
        )
        return JsonResponse(
            {
                "id_pdv": PDV.id_pdv,
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
        PDV_obj = PDV.objects.get(id_pdv=id)
        PDV_obj.nome = data["nome"]
        PDV_obj.dia = data["dia"]
        PDV_obj.saldo_inicial = data["saldo_inicial"]
        PDV_obj.saldo_final = data.get("saldo_final", PDV.saldo_final)
        PDV_obj.save()
        return JsonResponse(
            {
                "id_pdv": PDV_obj.id_pdv,
                "nome": PDV_obj.nome,
                "loja": PDV_obj.loja.id,
                "dia": PDV_obj.dia,
                "insert": PDV_obj.insert,
                "update": PDV_obj.update,
                "saldo_inicial": PDV_obj.saldo_inicial,
                "saldo_final": PDV_obj.saldo_final,
            }
        )

    @csrf_exempt
    def delete(self, request, id):
        PDV = PDV.objects.get(id_pdv=id)
        PDV.delete()
        return JsonResponse({"message": "Caixa deletada com sucesso!"})


class views_transacao_pdv:

    @staticmethod
    @Utils.verificar_permissoes(codigo_model="transacao")
    def lista_transacao(request):

        return render(request, "caixa/transacao/lista_transacao.html")
