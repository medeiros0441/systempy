from pathlib import Path
from dj_database_url import parse as db_url
from pathlib import Path
from decouple import config, Csv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Specify the full path to the .env file
ENV_FILE = BASE_DIR / ".env"

from django.core.exceptions import ImproperlyConfigured

try:

    SECRET_KEY = config(
        "SECRET_KEY",
        default="p@#j8^nhjt@8f7q898yck7$-jm7p--r*-ip#k*$v%%p$&%q$ol",
        cast=str,
    )
    DEBUG = config("DEBUG", default=True, cast=bool)
    ALLOWED_HOSTS = ["wmsolutions.azurewebsites.net", "*"]

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

except ImproperlyConfigured as e:
    print(f"Erro de configuração: {e}")

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

MIDDLEWARE_django = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE_app = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "app.middlewares.AtualizarDadosClienteMiddleware",
]
MIDDLEWARE = MIDDLEWARE_app + MIDDLEWARE_django

ROOT_URLCONF = "setup.urls"

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
import os

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/assents/"

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
