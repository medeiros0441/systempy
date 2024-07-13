from app.models import Usuario, Log, Sessao
from app.view.views_sessao import views_sessao
from app.view.views_erro import views_erro
from app.static import UserInfo
import uuid
import traceback
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import (
    HttpResponseServerError,
    JsonResponse,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
import logging
import re

logger = logging.getLogger(__name__)


# ErrorHandlerMiddleware
class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        error_message = str(exception)
        if request.headers.get("Accept") == "application/json":
            return JsonResponse({"error_message": error_message}, status=500)
        return render(request, "erro.html", {"error_message": error_message})


# ErrorLoggingMiddleware
class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception caught in middleware: {exception}", exc_info=True)

        if not settings.DEBUG:
            Log.objects.create(
                tipo="Erro",
                origem=request.path,
                descricao=str(exception),
                usuario=request.user if request.user.is_authenticated else None,
                ip_usuario=request.META.get("REMOTE_ADDR"),
            )

        if isinstance(exception, ObjectDoesNotExist):
            return redirect("erro_404")
        elif isinstance(exception, PermissionDenied):
            return redirect("erro_403")
        elif isinstance(exception, AttributeError):
            return redirect("erro_500")
        return HttpResponseServerError("Erro interno do servidor")


# NotFoundMiddleware
class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path and request.path.endswith("/"):
            new_path = request.path.rstrip("/")
            if new_path and new_path != request.path:
                return HttpResponsePermanentRedirect(new_path)
        if response.status_code == 404:
            return redirect("erro_404")
        return response


# AtualizarDadosClienteMiddleware
class AtualizarDadosClienteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            ip_cliente = request.META.get("REMOTE_ADDR")
            request.session["ip_cliente"] = ip_cliente
            request.session["navegador_cliente"] = request.META.get("HTTP_USER_AGENT")

            id_usuario = request.session.get("id_usuario")
            sessao = Sessao.objects.filter(ip_sessao=ip_cliente).first()

            if not sessao:
                views_sessao.criar_sessao(request)

            if sessao and sessao.pagina_atual != request.path:
                sessao.pagina_atual = request.path
                sessao.time_finalizou = timezone.now()
                sessao.save()

            if self.is_valid_uuid(id_usuario):
                sessao.id_usuario = id_usuario
                sessao.save()
                request.session["isCliente"] = True
                request.session["id_usuario"] = id_usuario
            else:
                request.session["isCliente"] = False

        except Exception as e:
            traceback_info = traceback.format_exc()
            error_message = f"Erro durante a autenticação: {str(e)}. Página: {request.path}. Linha: {traceback_info.splitlines()[-2]}"
            return views_erro.erro(request, error_message)

    def process_response(self, request, response):
        try:
            return response
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_message = f"Erro durante a autenticação: {str(e)}\n{traceback_str}"
            return views_erro.erro(request, error_message)

    def is_valid_uuid(self, val):
        try:
            if val is None:
                return False
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def is_exempted_url(self, path):
        urls_sem_verificacao = [
            r"^/$",
            r"^/login$",
            r"^/home$",
            r"^/cadastro$",
            r"^/sobre$",
            r"^/Erro$",
            r"^/enviar-codigo",
            r"^/confirmar-codigo",
            r"^/atualizar-senha",
            r"^/api/status_on",
            r"^/api/status_off",
            r"^/api_login",
        ]

        # Verificação usando expressões regulares
        is_exempt = any(re.match(pattern, path) for pattern in urls_sem_verificacao)

        # Print para depuração
        print(f"Verificando URL: {path}")
        print(f"URL '{path}' is exempt: {is_exempt}")

        return is_exempt
