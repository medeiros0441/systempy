from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import render, redirect


class views_erro:
    @staticmethod
    def erro(request, error_message):
        if request.headers.get("Accept") == "application/json":
            return JsonResponse({"error_message": error_message}, status=500)
        else:
            return render(request, "erro.html", {"error_message": error_message})
