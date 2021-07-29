import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("THOMANN_SECRET_KEY")


ALLOWED_HOSTS = []


DB_SCHEMA = os.getenv("THOMANN_DB_SCHEMA")
DB_NAME = os.getenv("THOMANN_DB_NAME")
DB_PORT = os.getenv("THOMANN_DB_PORT")
DB_USERNAME = os.getenv("THOMANN_DB_USERNAME")
DB_PASSWORD = os.getenv("THOMANN_DB_PASSWORD")
DB_HOST = os.getenv("THOMANN_DB_HOST")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "rest_framework",
    "ordered_model",
    "fontawesomefree",
    "lookup_hub",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "thomann.urls"

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


WSGI_APPLICATION = "thomann.wsgi.application"
ASGI_APPLICATION = "thomann.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "OPTIONS": {
            "options": f"-c search_path={DB_SCHEMA}"
        },
        "NAME": DB_NAME,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "USER": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
    }
}


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "{asctime} - {name} - {levelname} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "logs/warnings.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "lookup_hub": {
            "handlers": ["console", "file"],
            "propagate": True,
            "level": "DEBUG",
        },
    }
}
