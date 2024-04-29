from pathlib import Path
from decouple import config
import os
from django.core.exceptions import ImproperlyConfigured
from requests.exceptions import ConnectionError

# Determina o ambiente atual como produção
ENVIRONMENT = "production"

# Carrega as variáveis de ambiente para produção
from dotenv import load_dotenv
load_dotenv(".env.prod")

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = "setup.urls"
SESSION_COOKIE_AGE = 8 * 60 * 60

# Configurações do banco de dados
DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
    }
}

# Configurações gerais
import secrets

# Gera uma chave secreta aleatória
SECRET_KEY = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))

DEBUG = False
ALLOWED_HOSTS =  ["comercioprime.azurewebsites.net","*"]
 

# Lista de apps do Django
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Apps de terceiros
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
]

# Apps personalizados
MY_APPS = [
    "app",
]

INSTALLED_APPS = MY_APPS + THIRD_PARTY_APPS + DJANGO_APPS

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middlewares.AtualizarDadosClienteMiddleware",
    "app.middlewares.ErrorLoggingMiddleware",
]

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Senhas de validação
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configurações de localização e fuso horário
LANGUAGE_CODE = "pt-BR"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Diretórios estáticos
STATIC_URL = "assents/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Configuração para compressão de arquivos estáticos
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Configurações de segurança para produção
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CORS_ORIGIN_WHITELIST = ['https://comercioprime.azurewebsites.net']
