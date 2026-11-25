SECRET_KEY = "django-insecure-debugging-practice-only"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "urls"
MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "cors_middleware.CorsMiddleware",
]
APPEND_SLASH = False
USE_TZ = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS = [
    "django.contrib.contenttypes",
]
