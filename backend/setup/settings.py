from pathlib import Path
import os
from decouple import config
from dotenv import load_dotenv
from datetime import timedelta

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis de ambiente
ENVIRONMENT = os.getenv("DJANGO_ENV", "development")
load_dotenv(".env")

# Debug
DEBUG = ENVIRONMENT == "development"

# Hosts e Origens Permitidas
ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://comercioprime.azurewebsites.net",
    "http://comercioprime.azurewebsites.net",
]

CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "https://comercioprime.azurewebsites.net",
]


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "comercioprime.azurewebsites.net",
]

# Segurança
SECRET_KEY = config("SECRET_KEY") 

# Aplicações Instaladas
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
    'channels',
]

# JWT
SIMPLE_JWT = {
    
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("access",),
}

# Framework REST
REST_FRAMEWORK = {
      "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "api.permissions.CustomPermission",  # Permissão padrão
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
 
}

# Middleware
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

# CORS
CORS_ALLOW_HEADERS = [
    "content-type",
    "X-CSRFToken",
]

# CSRF
CSRF_COOKIE_NAME = "csrftoken"
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=False
CSRF_COOKIE_PATH = '/'  # O caminho deve ser '/' para cobrir todo o site
CSRF_COOKIE_DOMAIN = None  # Defina isso se estiver usando subdomínios, por exemplo, '.example.com'
# Webpack

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "build/",
        "STATS_FILE": os.path.join(BASE_DIR, "frontend", "webpack-stats.json"),
    }
}
# Templates
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

# WSGI
WSGI_APPLICATION = "setup.wsgi.application"
ASGI_APPLICATION = 'setup.asgi.application'

# Banco de Dados
# Obtenha o tipo de banco de dados do ambiente
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')

if DATABASE_TYPE == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', 'postgres'),
            'USER': os.getenv('DB_USER', 'user'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, os.getenv('SQLITE_NAME', 'db.sqlite3')),
        }
    }
# Senhas de Validação
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Localização e Fuso Horário
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = True
DATE_FORMAT = "d/m/Y"
DATETIME_FORMAT = "d/m/Y H:i"

# Diretórios Estáticos
STATIC_URL = "/static/"

ROOT_URLCONF = "setup.urls"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "frontend", "build", "static"),
]
# Segurança
# settings.py
import os

if DEBUG:
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
else:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
