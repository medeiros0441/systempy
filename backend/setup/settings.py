from pathlib import Path
from decouple import config
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "/static/"
# Carregar variáveis de ambiente do arquivo correspondente ao ambiente atual
ENVIRONMENT = os.getenv("DJANGO_ENV", "")
if ENVIRONMENT == "development":
    load_dotenv(".env")
    DEBUG = True
else:
    DEBUG = False
    load_dotenv(".env")
    CSRF_TRUSTED_ORIGINS = [
        "https://comercioprime.azurewebsites.net",
        "http://comercioprime.azurewebsites.net",
    ]
CORS_ALLOWED_ORIGINS = [
    "https://comercioprime.azurewebsites.net",
    "http://comercioprime.azurewebsites.net",
]

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "comercioprime.azurewebsites.net",
    "https://comercioprime.azurewebsites.net",
    "http://comercioprime.azurewebsites.net",
    "localhost",
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


from datetime import timedelta

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
    "api.middlewares.AtualizarDadosClienteMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "api.middlewares.ErrorLoggingMiddleware",
    "api.middlewares.ErrorHandlerMiddleware",
    "api.middlewares.NotFoundMiddleware",
]

ROOT_URLCONF = "setup.urls"

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
