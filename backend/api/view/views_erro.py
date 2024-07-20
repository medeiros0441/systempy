from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import render, redirect


class views_erro:
    @staticmethod
    def erro(request, error_message):
        return JsonResponse({"error_message": error_message}, status=500)
