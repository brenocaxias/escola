import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não definida nas variáveis de ambiente!")

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'escola-musica-groairas.up.railway.app').split(',')

CSRF_TRUSTED_ORIGINS = ['https://escola-musica-groairas.up.railway.app']

X_FRAME_OPTIONS = 'SAMEORIGIN'

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- APLICAÇÕES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'cursos',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'escola_de_musica.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'escola_de_musica.wsgi.application'

# --- BANCO DE DADOS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'emg_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- BACKBLAZE B2 (via S3 API) ---
AWS_ACCESS_KEY_ID = os.getenv('B2_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('B2_APP_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('B2_BUCKET_NAME', 'emg-materiais')
AWS_S3_ENDPOINT_URL = os.getenv('B2_ENDPOINT', 'https://s3.us-west-004.backblazeb2.com')
AWS_S3_REGION_NAME = 'us-west-004'
AWS_DEFAULT_ACL = None  # bucket privado — URLs assinadas
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = True       # gera URLs assinadas automaticamente
AWS_QUERYSTRING_EXPIRE = 3600     # URL válida por 1 hora
AWS_S3_FILE_OVERWRITE = False     # não sobrescreve arquivos com mesmo nome

# --- STORAGES ---
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# --- AUTENTICAÇÃO ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'login_sucesso'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = 'login'