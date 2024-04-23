from pathlib import Path
from dj_database_url import parse as db_url
from decouple import config
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Specify the full path to the .env file
ENV_FILE = BASE_DIR / ".env"

try:
    ROOT_URLCONF = "setup.urls"

    WSGI_APPLICATION = "setup.wsgi.application"

    SECRET_KEY = config(
        "SECRET_KEY",
        default="p@#j8^nhjt@8f7q898yck7$-jm7p--r*-ip#k*$v%%p$&%q$ol",
        cast=str,
    )
    DEBUG = False
    ALLOWED_HOSTS = ["comercioprime.azurewebsites.net", "*"]

    # Database
    DATABASES = {
        "default": {
            "ENGINE": config(
                "DB_ENGINE", default="django.db.backends.postgresql", cast=str
            ),
            "NAME": config("DB_NAME", default="postgres", cast=str),
            "USER": config("DB_USER", default="wmsdatabase", cast=str),
            "PASSWORD": config("DB_PASSWORD", default="dmmZhUCBWvcMxIMuriHO", cast=str),
            "HOST": config(
                "DB_HOST",
                default="wms.cnkmy2e26ipt.us-east-1.rds.amazonaws.com",
                cast=str,
            ),
            "PORT": config("DB_PORT", default=5432, cast=int),
        }
    }

    DJANGO_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    THIRD_PARTY_APPS = [
        "crispy_forms",
        "crispy_bootstrap5",
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

    CRISPY_TEMPLATE_PACK = "bootstrap5"

    MY_APPS = [
        # integracao do app
        "app",
    ]

    INSTALLED_APPS = MY_APPS + THIRD_PARTY_APPS + DJANGO_APPS
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

    LANGUAGE_CODE = "pt-BR"

    TIME_ZONE = "America/Sao_Paulo"

    USE_I18N = True

    USE_TZ = True

    BASE_DIR = Path(__file__).resolve().parent.parent
    STATIC_URL = "assents/"

    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    # Configure o armazenamento para compressão de arquivos estáticos

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Habilitar a compressão de arquivos CSS e JavaScript
    COMPRESS_ENABLED = True

    # Executar a compressão de arquivos estáticos offline durante a coleta de arquivos estáticos
    COMPRESS_OFFLINE = True
    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"
    if DEBUG == True:
        SESSION_COOKIE_SECURE = False
        CSRF_COOKIE_SECURE = False
        SECURE_SSL_REDIRECT = False
    elif DEBUG == False:
        # Configuração para o tempo de vida da política HSTS
        SECURE_HSTS_SECONDS = 31536000  # 1 ano
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

        # Redirecionamento automático para HTTPS
        SECURE_SSL_REDIRECT = True

        # Configurações para cookies de sessão e CSRF
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True

except ImproperlyConfigured as e:
    print(f"Erro de configuração: {e}")
