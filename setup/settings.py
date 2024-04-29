from pathlib import Path
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

ENVIRONMENT = "production"

if ENVIRONMENT == "production":
    load_dotenv(".env.prod")


DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["*" ,"comercioprime.azurewebsites.net"]
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
]

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

STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    # In production, collect static files to a single directory
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
