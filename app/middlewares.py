# middleware.py
from django.shortcuts import redirect
from .def_global import erro, criar_alerta_js


class ClienteDefaultMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o caminho do URL começa com "cliente/default"
        if request.path.startswith("/cliente/default"):
            # Verifica se os dados na sessão são diferentes de zero
            if (
                request.session.get("id_usuario", 0) == 0
                or request.session.get("id_empresa", 0) == 0
                or request.session.get("nivel_usuario", 0) == 0
            ):
                # Se algum dos dados for zero, redireciona para outra página
                return redirect(
                    "", {"alerta": criar_alerta_js("Você precisa fazer o login")}
                )

        response = self.get_response(request)
        return response


from django.utils.deprecation import MiddlewareMixin
from .models import SessaoUsuario
from django.utils import timezone


class AtualizarDadosClienteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.get("id_usuario"):
            id_usuario = request.session.get("id_usuario")
            if id_usuario:
                ip_cliente = request.META.get("REMOTE_ADDR")
                navegador_cliente = request.META.get("HTTP_USER_AGENT")
                # Atualizar os dados do cliente no banco de dados
                sessao_usuario, created = SessaoUsuario.objects.get_or_create(
                    usuario=id_usuario
                )
                sessao_usuario.ip_cliente = ip_cliente
                sessao_usuario.navegador_cliente = navegador_cliente
                sessao_usuario.save()

    def process_response(self, request, response):
        if request.session.get("id_usuario"):
            # Se o usuário está autenticado, atualize a última atividade ou faça outras ações de saída
            id_usuario = request.session.get("id_usuario")
            sessao_usuario = SessaoUsuario.objects.get(usuario=id_usuario)
            sessao_usuario.ultima_atividade = timezone.now()
            sessao_usuario.save()
        return response
