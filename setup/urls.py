# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

app_name = "app"

urlpatterns = [
    path("admin/", admin.site.urls),  # URL do site administrativo do Django
    path("", include("setup.urls_public")),  # Inclui URLs públicas na raiz
    path(
        "admin-dashboard/", include("setup.urls_admin")
    ),  # Inclui URLs administrativas
]

# Se você quiser adicionar as configurações para servir arquivos estáticos em modo DEBUG
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
