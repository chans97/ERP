"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "cssd1xkjewhis51ukzwo03)ebo2$rdb_p8ve8tz3jcx=j_^bk*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
PROJECT_APPS = [
    "users.apps.UsersConfig",
    "StandardInformation.apps.StandardInformationConfig",
    "core.apps.CoreConfig",
    "orders.apps.OrdersConfig",
    "producemanages.apps.ProducemanagesConfig",
    "qualitycontrols.apps.QualitycontrolsConfig",
    "stockmanages.apps.StockmanagesConfig",
    "measures.apps.MeasuresConfig",
    "specials.apps.SpecialsConfig",
    "afterservices.apps.AfterservicesConfig",
    "stocksingle.apps.StocksingleConfig",
    "stockrack.apps.StockrackConfig",
    "parts.apps.PartsConfig",
]

THIRD_PARTY_APPS = ["django_seed"]


INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "mysite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "erpdemo.cygkdjtf3dkq.ap-northeast-2.rds.amazonaws.com",
        "NAME": "erpdemo",
        "USER": "postgresql",
        "PASSWORD": "ckstn11!!",
        "PORT": "5432",
    }
}
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

"""
DATABASES = {
 'default': {
  'ENGINE': 'sql_server.pyodbc',
  'NAME': 'mydb',
  'HOST': '127.0.0.1',
  'OPTIONS': {
    'driver' : 'SQL Server Native Client 11.0',
    'MARS_Connection' : True,
    'dsn' : 'mydb',
    'driver_supports_utf8' : True,
        },
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "/media/"

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "static"))
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
AUTH_USER_MODEL = "users.User"
