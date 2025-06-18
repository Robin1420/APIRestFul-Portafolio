"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Añadir el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Configurar el entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cargar variables de entorno desde .env si existe
from dotenv import load_dotenv
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# Configurar logging
import logging
logger = logging.getLogger(__name__)
try:
    logger.info("Iniciando aplicación WSGI")
    logger.info(f"Directorio base: {BASE_DIR}")
    logger.info(f"Módulo de configuración: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
except Exception as e:
    print(f"Error al configurar logging: {e}")

# Obtener la aplicación WSGI
application = get_wsgi_application()
