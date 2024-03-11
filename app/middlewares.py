# middleware.py
from django.shortcuts import redirect, get_object_or_404
from .def_global import erro, criar_alerta_js
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import HttpRequest
from app.models import Usuario ,Log,Sessao
from django.utils import timezone
from django.conf import settings

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not settings.DEBUG:  # Verifica se o modo de depuração está ativado
            # Registra o erro no modelo Log
            Log.objects.create(
                tipo='Erro',
                origem=request.path,
                descricao=str(exception),
                usuario=request.user if request.user.is_authenticated else None,
                ip_usuario=request.sessao['ip_usuario']
            )
class AtualizarDadosClienteMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        ip_cliente = request.META.get("REMOTE_ADDR")
        navegador_cliente = request.META.get("HTTP_USER_AGENT")

        # Obtém o ID do usuário da sessão
        id_usuario = request.session.get("id_usuario")
        
        request.session["ip_cliente"] = ip_cliente
        request.session["navegador_cliente"] = navegador_cliente
        
        
        # Se o ID do usuário não estiver presente, define como 0
        if id_usuario is None:
            id_usuario = 0
            request.session["id_usuario"] = 0
        # Verifica se o IP do cliente está cadastrado em sessão
        sessao_usuario = Sessao.objects.filter(ip_sessao=ip_cliente).first()

        # Se o IP do cliente não estiver cadastrado, cria uma nova sessão
        if not sessao_usuario:
            sessao_usuario = Sessao.objects.create(
                ip_sessao=ip_cliente,
                descricao=navegador_cliente,
                status=True,
            )

        # Se o ID do usuário for diferente do atual, atualiza com o novo ID
        if sessao_usuario.usuario_id != id_usuario and id_usuario > 0:
            sessao_usuario.usuario_id = id_usuario
            sessao_usuario.save()
            # Se a página atual for diferente da cadastrada, atualiza com a nova página
            if sessao_usuario.pagina_atual != request.path:
                sessao_usuario.pagina_atual = request.path
                sessao_usuario.time_finalizou = timezone.now()
                sessao_usuario.save()

        # Define o cookie isCliente baseado no ID do usuário
        if id_usuario > 0:
            request.session["isCliente"] = True
            request.session["id_usuario"] = id_usuario
        else:
            request.session["isCliente"] = False

    def process_response(self, request, response):
        if request.session.get("id_usuario"):
            # Se o usuário está autenticado, atualize a última atividade no banco de dados
            id_usuario = request.session.get("id_usuario")
            usuario = get_object_or_404(Usuario, pk=id_usuario)
            empresa = usuario.empresa
            if empresa.id_empresa:
                request.session["id_empresa"] = int(empresa.id_empresa)
            sessao_usuario = Sessao.objects.get(usuario_id=id_usuario)
            sessao_usuario.time_finalizou = timezone.now()
            sessao_usuario.save()
            if id_usuario > 0:
                request.session["isCliente"] = True
                request.session["id_usuario"] = id_usuario
        return response

    #   if isAssinante(request) == False:
    # return render(request, "default/sobre.html", {"alerta_js": criar_alerta_js("Você precisa autenticar-se")})
