from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para la seguridad del proyecto
SECRET_KEY = 'django-insecure-k$5vbptubfqbm55m6hf8-d@zm+_u2xq(cv73&l7jq)kqn3geh1'

# Activar el modo de desarrollo
DEBUG = True

# Definir los hosts permitidos
ALLOWED_HOSTS = []

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',         # Panel de administración de Django
    'django.contrib.auth',           # Sistema de autenticación
    'django.contrib.contenttypes',   # Soporte de tipos de contenido
    'django.contrib.sessions',       # Manejo de sesiones
    'django.contrib.messages',       # Sistema de mensajes
    'django.contrib.staticfiles',    # Archivos estáticos
    'biblioteca',                    # La aplicación 'biblioteca' (tu app personalizada)
]

# Middleware para manejo de solicitudes y respuestas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs raíz del proyecto
ROOT_URLCONF = 'biblioteca_project.urls'

# Configuración de plantillas (templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'biblioteca' / 'templates'],
        'APP_DIRS': True,  # Activa la búsqueda de templates en las carpetas de las aplicaciones
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application para servir el proyecto
WSGI_APPLICATION = 'biblioteca_project.wsgi.application'

# Base de datos MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Usando MySQL como base de datos
        'NAME': 'biblioteca',  # Nombre de la base de datos
        'USER': 'root',        # Usuario de MySQL
        'PASSWORD': 'Studium2023;',  # Contraseña del usuario MySQL
        'HOST': 'localhost',   # Dirección del servidor de la base de datos
        'PORT': '3306',        # Puerto de MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # Configuración adicional
        }
    }
}

# Validadores de contraseñas
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

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'

# Internacionalización y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, Imágenes)
STATIC_URL = 'static/'
LOGOUT_REDIRECT_URL = '/accounts/login/'  # O a donde quieras redirigir después del logout


# Tipo de campo de clave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
