SECRET_KEY = "practice"
DEBUG = True
ROOT_URLCONF = "config.urls"
ALLOWED_HOSTS = ["*"]
MIDDLEWARE = ["api.middleware.AuthMiddleware"]
INSTALLED_APPS = ["django.contrib.contenttypes", "api"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

STATIC_URL = "static/"


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
