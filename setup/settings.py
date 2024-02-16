from pathlib import Path
from decouple import config, Csv
from dj_database_url import parse as db_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

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
# Application definition

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
    # Outros middlewares...
    "app.middlewares.ClienteDefaultMiddleware",
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

WSGI_APPLICATION = "systempy.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
from pathlib import Path

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração do banco de dados
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "wmsdatabase",
        "PASSWORD": "dmmZhUCBWvcMxIMuriHO",
        "HOST": "wms.cnkmy2e26ipt.us-east-1.rds.amazonaws.com",
        "PORT": "5432",  # Porta padrão para PostgreSQL
    },
    "test": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/assents/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


import xml.etree.ElementTree as ET

# Define o caminho para o arquivo de publicação
PUBLISH_PROFILES_XML_PATH = "publish/publish_profiles.xml"


# Lê os dados do arquivo de publicação
def read_publish_profiles():
    tree = ET.parse(PUBLISH_PROFILES_XML_PATH)
    root = tree.getroot()

    # Itera sobre os elementos de publicação
    for profile in root.findall("publishProfile"):
        profile_name = profile.get("profileName")
        publish_method = profile.get("publishMethod")
        publish_url = profile.get("publishUrl")
        # ... você pode processar outros atributos conforme necessário
        print(
            f"Profile Name: {profile_name}, Publish Method: {publish_method}, Publish URL: {publish_url}"
        )
