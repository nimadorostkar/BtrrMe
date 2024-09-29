from pathlib import Path
import environ
import os

env_file = Path(__file__).resolve().parent.parent / '.env'
env = environ.Env()
env.read_env(env_file)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ['localhost','127.0.0.1','api.btrr.me','btrr.me']
SITE_ID = 1



# APP CONFIGURATION
DJANGO_APPS = (
    "daphne",
    "chat",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "channels",
)
THIRD_PARTY_APPS = (
    "rest_framework",
    "django_filters",
    "corsheaders",
    "gunicorn",
    "whitenoise",
    "django.contrib.sites",
    "ckeditor",
    "ckeditor_uploader",
    "import_export",
    "rest_framework_swagger",
    "drf_yasg",
    "storages",
)
LOCAL_APPS = (
    "accounts",
    "nutrition",
    "workout",
    "supplement",
    "blog",
    "program",
    "contact",
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# END APP CONFIGURATION

#WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
ROOT_URLCONF = "config.urls"
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates/",
        ],
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



# DATABASE CONFIGURATION
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}
# END DATABASE CONFIGURATION


# CACHING CONFIGURATION
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL"),
    }
}
# END CACHING CONFIGURATION


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts":[{
                "address": os.getenv('REDIS_URL'),
            }]}
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]



MAX_UPLOAD_SIZE = 5242880
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"



# S3 Settings
LIARA_ENDPOINT="https://storage.iran.liara.space"
LIARA_BUCKET_NAME="btrrme"
LIARA_ACCESS_KEY="6ntrqdo07o5hkagq"
LIARA_SECRET_KEY="5a91b406-9602-486e-bb94-f65a92e6f91a"

# S3 Settings Based on AWS (optional)
AWS_ACCESS_KEY_ID = LIARA_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = LIARA_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = LIARA_BUCKET_NAME
AWS_S3_ENDPOINT_URL = LIARA_ENDPOINT
AWS_S3_REGION_NAME = 'us-east-1'

# Django-storages configuration
STORAGES = {
  "default": {
      "BACKEND": "storages.backends.s3.S3Storage",
  },
  "OPTIONS": {
            "location": "media/",
  },
  "staticfiles": {
      "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
  },
}

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "docs")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = "https://btrrme.storage.iran.liara.space/media/"
MEDIA_URL = "https://btrrme.storage.iran.liara.space/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"




# OTP CONFIGURATION
OTP_CODE_LENGTH = int(env("OTP_CODE_LENGTH", default="4"))
OTP_TTL = int(env("OTP_TTL", default="120"))
# END OTP CONFIGURATION

# JWT SETIINGS
ACCESS_TTL = int(env("ACCESS_TTL", default="1"))  # days
REFRESH_TTL = int(env("REFRESH_TTL", default="5"))  # days
JWT_SECRET = env("SECRET_KEY")
# END JWT SETTINGS



# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "accounts.backends.JWTAuthentication",
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_THROTTLE_RATES": {"otp": env("OTP_THROTTLE_RATE", default="10/min"), },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
# END REST FRAMEWORK CONFIGURATION


# CORSHEADERS CONFIGURATION
CORS_ALLOWED_ORIGINS = ['http://localhost','http://127.0.0.1','https://btrr.me','https://api.btrr.me']
CSRF_TRUSTED_ORIGINS = ['http://localhost','http://127.0.0.1','https://btrr.me','https://api.btrr.me']
CORS_ORIGIN_ALLOW_ALL = True
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True
# END CORSHEADERS CONFIGURATION


# SMS CONFIGURATION
KAVENEGAR_API_KEY = env("KAVENEGAR_API_KEY")
KAVENEGAR_TEMPLATE = env("KAVENEGAR_TEMPLATE")
# END SMS CONFIGURATION

APPEND_SLASH = True