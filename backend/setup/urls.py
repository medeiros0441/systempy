# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

urlpatterns = [
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html")),  # Rota do React
    # Servir o React index.html
]
