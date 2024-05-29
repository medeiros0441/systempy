from pathlib import Path
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo correspondente ao ambiente atual
ENVIRONMENT = os.getenv("DJANGO_ENV", "")
if ENVIRONMENT == "development":
    load_dotenv(".env_dev")
    DEBUG = True
else:
    DEBUG = False
    load_dotenv(".env")
    CSRF_TRUSTED_ORIGINS = [
        "https://comercioprime.azurewebsites.net",
        "http://comercioprime.azurewebsites.net",
    ]
ALLOWED_HOSTS = [
    "*",
    "https://comercioprime.azurewebsites.net",
    "http://comercioprime.azurewebsites.net",
]
SECRET_KEY = "p@#j8^nhjt@8f7q898yck7$-jm7p--r*-ip#k*$v%%p$&%q$ol"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "app",
    "corsheaders",
    "django_extensions",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "app.middlewares.AtualizarDadosClienteMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middlewares.ErrorLoggingMiddleware",
    "app.middlewares.ErrorHandlerMiddleware",
    "app.middlewares.NotFoundMiddleware",
]

ROOT_URLCONF = "setup.urls"
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
STATIC_URL = "assents/"

APP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.dirname(APP_DIR)
STATIC_ROOT = os.path.join(APP_ROOT, "app", "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# Configurações de segurança
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else:

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
