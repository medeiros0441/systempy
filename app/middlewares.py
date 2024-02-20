# middleware.py
from django.shortcuts import redirect
from .def_global import erro, criar_alerta_js
from django.utils.deprecation import MiddlewareMixin
from .models.sessao import Sessao
from django.utils import timezone
from django.http import HttpRequest


class AtualizarDadosClienteMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        ip_cliente = request.META.get("REMOTE_ADDR")
        navegador_cliente = request.META.get("HTTP_USER_AGENT")

        # Obtém o ID do usuário da sessão
        id_usuario = request.session.get("id_usuario")

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

        # Se a página atual for diferente da cadastrada, atualiza com a nova página
        if sessao_usuario.pagina_atual != request.path:
            sessao_usuario.pagina_atual = request.path
            sessao_usuario.time_finalizou = timezone.now()
            sessao_usuario.save()

        # Se o ID do usuário for diferente do atual, atualiza com o novo ID
        if sessao_usuario.usuario_id != id_usuario and id_usuario > 0:
            sessao_usuario.usuario_id = id_usuario
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
            sessao_usuario = Sessao.objects.get(usuario_id=id_usuario)
            sessao_usuario.time_finalizou = timezone.now()
            sessao_usuario.save()
        return response
