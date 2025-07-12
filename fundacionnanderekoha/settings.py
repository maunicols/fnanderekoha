from pathlib import Path
import os 
from dotenv import load_dotenv
import logging

# load .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'invalid_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG_ENABLED', 'False') # Ajusta esto según tu dominio

# Log DEBUG status
logger = logging.getLogger(__name__)
logger.info(f"DEBUG mode is {'ENABLED' if DEBUG else 'DISABLED'}")

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'https://fnanderekoha-production.up.railway.app/' 'fnanderekoha-production.up.railway.app'] # Ajusta esto según tu dominio

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #myapps
    'landing',
    'users',
    'dashboard',
    'news',
    #modules
    'crispy_forms',
    'crispy_bootstrap5',
    'bootstrap5',



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agregar WhiteNoise
    'fundacionnanderekoha.middleware.DebugLogMiddleware',  # Custom debug logging middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fundacionnanderekoha.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fundacionnanderekoha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', os.getenv('PGDATABASE', 'fnanderekoha_db')),
        'USER': os.getenv('DB_USER', os.getenv('PGUSER', 'fnanderekoha_user')),
        'PASSWORD': os.getenv('DB_PASSWORD', os.getenv('PGPASSWORD', 'fnanderekoha_password')),
        'URL': os.getenv('DATABASE_URL', os.getenv('DATABASE_URL', 'postgres://fnanderekoha_user:fnanderekoha_password@localhost:5432/fnanderekoha_db')),
        'HOST': os.getenv('DB_HOST', os.getenv('PGHOST', 'localhost')),
        'PORT': os.getenv('DB_PORT', os.getenv('PGPORT', '5432')),
        'CONN_MAX_AGE': 0,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# CRISPY FORMS SETTINGS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-Ar'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración de WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', "False")  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', "os.getenv('PGDATABASE', 'fnanderekoha_db')")  # Set to True in production with HTTPS

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth settings
LOGIN_REDIRECT_URL = 'dashboard:home'  # Redirigir al dashboard después del login
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'landing-home'  # Redirigir al landing después del logout
