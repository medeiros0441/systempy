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
