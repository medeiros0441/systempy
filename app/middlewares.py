# middleware.py
from django.shortcuts import redirect, get_object_or_404
from .utils import utils
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import HttpRequest
from app.models import Usuario, Log, Sessao
from django.utils import timezone
from django.conf import settings
from .view import views_sessao
from .static import UserInfo
from django.core.exceptions import ObjectDoesNotExist
import traceback


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            if not settings.DEBUG:
                # Registra o erro no modelo Log
                Log.objects.create(
                    tipo="Erro",
                    origem=request.path,
                    descricao=str(exception),
                    usuario=request.user if request.user.is_authenticated else None,
                    ip_usuario=request.sessao["ip_usuario"],
                )
        else:
            return None  #


class AtualizarDadosClienteMiddleware(MiddlewareMixin):
    # process_request é chamado antes da view ser executada e recebe apenas a solicitação.
    def process_request(self, request: HttpRequest):
        try:

            ip_cliente = request.META.get("REMOTE_ADDR")
            navegador_cliente = request.META.get("HTTP_USER_AGENT")
            request.session["ip_cliente"] = ip_cliente
            request.session["navegador_cliente"] = navegador_cliente

            # Obtém o ID do usuário da sessão
            id_usuario = request.session.get("id_usuario")

            # Se o ID do usuário não estiver presente, define como 0
            if id_usuario is None:
                id_usuario = 0
                request.session["id_usuario"] = 0
            # Verifica se o IP do cliente está cadastrado em sessão
            sessao = Sessao.objects.filter(ip_sessao=ip_cliente).first()

            # Se o IP do cliente não estiver cadastrado, cria uma nova sessão
            if not sessao:
                views_sessao.criar_sessao(request)

            # Se o ID do usuário for diferente do atual, atualiza com o novo ID
            if sessao is not None:
                if sessao.pagina_atual != request.path:
                    sessao.pagina_atual = request.path
                    sessao.time_finalizou = timezone.now()
                    sessao.save()
                if id_usuario > 0:
                    sessao.id_usuario = id_usuario
                    sessao.save()
                    # Se a página atual for diferente da cadastrada, atualiza com a nova página

            # Define o cookie isCliente baseado no ID do usuário
            if id_usuario > 0:
                request.session["isCliente"] = True
                request.session["id_usuario"] = id_usuario
            else:
                request.session["isCliente"] = False

            # Lista de URLs sem verificação
            urls_sem_verificacao = [
                "",
                "/login/",
                "/home",
                "/cadastro/",
                "/login/",
                "/sobre/",
                "/Erro/",
            ]

            # URLs com valores variáveis
            url_funcJs = [
                "enviar-codigo/<str:email>/",
                "confirmar-codigo/<str:codigo>/",
                "atualizar-senha/<str:nova_senha>/",
                "api/status_on/",
                "api/status_off/",
            ]

            # Remover as partes dos valores variáveis das URLs de url_funcJs e adicionar à lista urls_sem_verificacao
            for url_pattern in url_funcJs:
                urls_sem_verificacao.append(url_pattern.split("<")[0])

            # Verificar se a URL atual não está na lista de URLs sem verificação
            if not any(request.path.startswith(url) for url in urls_sem_verificacao):
                id_empresa = UserInfo.get_id_empresa(request, True)
                if id_empresa is None:
                    return redirect("login")

        except Exception as e:
            traceback_info = traceback.format_exc()
            # Constrói a mensagem de erro com a página e a linha específica
            error_message = f"Erro durante a autenticação: {str(e)}. Página: {request.path}. Linha: {traceback_info.splitlines()[-2]}"
            # Se ocorrer algum erro inesperado, execute a função de erro grave e registre o erro
            return utils.erro(request,error_message)

    def process_response(self, request, response):
        try:
            id_usuario = request.session.get("id_usuario", 0)
            if id_usuario > 0:
                usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
                empresa = usuario.empresa
                if empresa.id_empresa:
                    request.session["id_empresa"] = int(empresa.id_empresa)
                ip = request.META.get("REMOTE_ADDR")
                sessao, created = Sessao.objects.get_or_create(ip_sessao=ip)
                sessao.usuario = usuario
               # sessao.time_finalizou = timezone.now()
                sessao.save()
                request.session["isCliente"] = True
                request.session["id_usuario"] = id_usuario
            return response
        except Exception as e:
            traceback_str = traceback.format_exc()
            error_message = f"Erro durante a autenticação: {str(e)}\n{traceback_str}"
            return utils.erro(request, error_message)