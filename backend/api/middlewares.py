import logging
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token

# Configure o logger
logger = logging.getLogger(__name__)

class Middleware(MiddlewareMixin):
    def process_request(self, request):
        # Obtém o token CSRF do cabeçalho
        csrf_token_from_header = request.headers.get('X-CSRFToken')
        
        # Obtém o token CSRF esperado
        expected_token = get_token(request)
        
        # Log dos tokens para depuração
        logger.warning(f"Token CSRF enviado pelo React: {csrf_token_from_header}")
        logger.warning(f"Token CSRF esperado pelo Django: {expected_token}")
        
        # Verifica se o token CSRF está correto
        if csrf_token_from_header and csrf_token_from_header != expected_token:
            logger.warning("Token CSRF enviado não corresponde ao esperado.")
        elif not csrf_token_from_header:
            logger.warning("Token CSRF não enviado na requisição.")

        return None  # Continua o processamento normal da view

    