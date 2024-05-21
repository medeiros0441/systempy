from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import render, redirect


class views_erro:
    def erro(request, error_message):
        if request.headers.get("Accept") == "application/json":
            # Se a solicitação aceitar JSON, retorne um JsonResponse com a mensagem de erro
            return JsonResponse({"error_message": error_message}, status=500)
        else:
            # Caso contrário, retorne o template HTML para exibir a mensagem de erro na página
            return render(request, "Erro.html", {"error_message": error_message})
