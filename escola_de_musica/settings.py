import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURANÇA ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-he8qc3tc6w$gkrkmnovhc!n87(=x$qit51)iz%5ibxs=wxlvzc')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://escola-production-d4e0.up.railway.app']

# --- APLICAÇÕES ---
INSTALLED_APPS = [
    'cloudinary_storage',           # Deve ser o primeiro
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic', 
    'cursos'
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essencial para a Logo/Maestro
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

# --- BANCO DE DADOS (MYSQL RAILWAY) ---
# --- BANCO DE DADOS (Configuração Híbrida) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'emg_db'),        # 'emg_db' é o nome local
        'USER': os.getenv('DB_USER', 'root'),          # 'root' é o usuário local
        'PASSWORD': os.getenv('DB_PASSWORD', 'Caxias0404'), # Sua senha do Workbench
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),     # Localhost
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS E MÍDIA ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cursos', 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- CONFIGURAÇÃO CLOUDINARY ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'), # Use o seu Cloud Name aqui
    'API_KEY': os.getenv('API_KEY'),   # Use sua API Key
    'API_SECRET': os.getenv('API_SECRET'), # Coloque sua Secret real
}

# --- ARMAZENAMENTO (STORAGES) ---
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

# Linha extra para garantir compatibilidade com o app cloudinary_storage
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"

# --- AUTENTICAÇÃO ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'login_sucesso'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = 'login'

#limpeza do git test