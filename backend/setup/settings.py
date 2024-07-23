from pathlib import Path
from decouple import config
import os
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"

# Carregar variáveis de ambiente do arquivo correspondente ao ambiente atual
ENVIRONMENT = os.getenv("DJANGO_ENV", "")
load_dotenv(".env")  # Carrega o arquivo .env para todas as variáveis de ambiente

if ENVIRONMENT == "development":
    DEBUG = True
else:
    DEBUG = False

# Defina a lista de origens permitidas
ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://comercioprime.azurewebsites.net",
    "http://comercioprime.azurewebsites.net",
]

CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = ALLOWED_ORIGINS

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "comercioprime.azurewebsites.net",
]

SECRET_KEY = config("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "api",
    "corsheaders",
    "django_extensions",
    "webpack_loader",
    "rest_framework",
    "rest_framework_simplejwt",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "api.middlewares.Middleware",
]

ROOT_URLCONF = "setup.urls"
CSRF_COOKIE_NAME = "csrftoken"


WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "build/",  # Diretorio onde os arquivos compilados serão colocados
        "STATS_FILE": os.path.join(BASE_DIR, "frontend", "webpack-stats.json"),
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "..", "frontend", "build")],
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

WSGI_APPLICATION = "setup.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
SESSION_COOKIE_AGE = 8 * 60 * 60

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

USE_L10N = True

USE_TZ = True
# Diretórios estáticos
STATIC_URL = "assets/"

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "frontend", "build", "static"),
]

# Configurações de segurança
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = False
    # Redireciona todas as solicitações HTTP para HTTPS
    # Isso garante que todas as comunicações com o servidor sejam seguras.
    SECURE_SSL_REDIRECT = True

    # Configura o cabeçalho HTTP Strict Transport Security (HSTS) com um tempo de validade
    # HSTS informa aos navegadores para sempre usar HTTPS ao se conectar ao site.
    # O valor 3600 define o tempo em segundos (1 hora) durante o qual os navegadores devem manter a política HSTS.
    SECURE_HSTS_SECONDS = 3600

    # Inclui subdomínios no cabeçalho HSTS
    # Garante que todos os subdomínios também sigam a política HSTS.
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Adiciona o domínio ao preload list do HSTS
    # Isso faz com que o navegador trate o site como sempre HTTPS mesmo antes da primeira visita.
    SECURE_HSTS_PRELOAD = True

    # Ativa o filtro XSS (Cross-Site Scripting) no navegador
    # Protege contra ataques que injetam scripts maliciosos em páginas da web.
    SECURE_BROWSER_XSS_FILTER = True

    # Impede que os navegadores detectem o tipo de conteúdo de maneira insegura
    # Protege contra ataques de tipo de conteúdo, onde o navegador pode tentar interpretar dados maliciosos.
    SECURE_CONTENT_TYPE_NOSNIFF = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
