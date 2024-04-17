from config.settings.common import *

# PRODUCTION APPS CONFIGURATION
#INSTALLED_APPS += ("corsheaders", "gunicorn")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env("SECRET_KEY")
#ALLOWED_HOSTS = get_env("ALLOWED_HOSTS").split(",")
ALLOWED_HOSTS = ['localhost','127.0.0.1']

# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env("POSTGRES_DB"),
        "USER": get_env("POSTGRES_USER"),
        "PASSWORD": get_env("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": 5432,
    }
}
# END DATABASE CONFIGURATION


# CORSHEADERS CONFIGURATION
CORS_ALLOWED_ORIGINS = ["http://localhost", "http://127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://127.0.0.1"]

CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
MIDDLEWARE += ("corsheaders.middleware.CorsMiddleware",)
# END CORSHEADERS CONFIGURATION
DEBUG = get_env("DEBUG") == "True"

JWT_SECRET = get_env("JWT_SECRET", default=SECRET_KEY)

