from django.shortcuts import redirect, get_object_or_404
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import HttpRequest
from app.models import Usuario, Log, Sessao
from app.view.views_sessao import views_sessao
from app.view.views_erro import views_erro
from app.static import UserInfo
from django.core.exceptions import ObjectDoesNotExist
import traceback
from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import redirect

import logging

logger = logging.getLogger(__name__)


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
        else:
            return render(request, "erro.html", {"error_message": error_message})


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
        else:
            return HttpResponseServerError("Erro interno do servidor")


from django.http import HttpResponsePermanentRedirect


class NotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Verificar se o caminho da URL tem uma barra no final
        if request.path != "/" and request.path.endswith("/"):
            # Remover a barra no final
            new_path = request.path.rstrip("/")
            # Verificar se a nova URL corresponde a uma view
            if new_path and new_path != request.path:
                return HttpResponsePermanentRedirect(new_path)
        if response.status_code == 404:
            return redirect("erro_404")
        return response


# AtualizarDadosClienteMiddleware
class AtualizarDadosClienteMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        try:
            ip_cliente = request.META.get("REMOTE_ADDR")
            navegador_cliente = request.META.get("HTTP_USER_AGENT")
            request.session["ip_cliente"] = ip_cliente
            request.session["navegador_cliente"] = navegador_cliente

            id_usuario = request.session.get("id_usuario")
            if id_usuario is None:
                id_usuario = 0
                request.session["id_usuario"] = 0

            sessao = Sessao.objects.filter(ip_sessao=ip_cliente).first()
            if not sessao:
                views_sessao.criar_sessao(request)

            if sessao is not None:
                if sessao.pagina_atual != request.path:
                    sessao.pagina_atual = request.path
                    sessao.time_finalizou = timezone.now()
                    sessao.save()
                if id_usuario > 0:
                    sessao.id_usuario = id_usuario
                    sessao.save()

            if id_usuario > 0:
                request.session["isCliente"] = True
                request.session["id_usuario"] = id_usuario
            else:
                request.session["isCliente"] = False

            urls_sem_verificacao = [
                "",
                "/login/",
                "/home",
                "/cadastro/",
                "/login/",
                "/sobre/",
                "/Erro/",
            ]

            url_funcJs = [
                "enviar-codigo/<str:email>/",
                "confirmar-codigo/<str:codigo>/",
                "atualizar-senha/<str:nova_senha>/",
                "api/status_on/",
                "api/status_off/",
            ]

            for url_pattern in url_funcJs:
                urls_sem_verificacao.append(url_pattern.split("<")[0])

            if not any(request.path.startswith(url) for url in urls_sem_verificacao):
                id_empresa = UserInfo.get_id_empresa(request, True)
                if id_empresa is None:
                    return redirect("login")

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
