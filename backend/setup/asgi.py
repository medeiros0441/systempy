import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.urls_api import websocket_urlpatterns  # Ajuste o caminho para o módulo correto

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
