# API Portafolio

API REST para el portafolio personal, desarrollada con Django REST Framework y conectada a una base de datos SQL Server en Somee.

## Requisitos

- Python 3.8+
- Docker (opcional, para despliegue)
- ODBC Driver 17 for SQL Server

## Configuración del entorno

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd API-Portafolio
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   - Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:
     ```
     SOMEE_CONNECTION_STRING=workstation id=portafolio.mssql.somee.com;packet size=4096;user id=usuario;pwd=contraseña;data source=portafolio.mssql.somee.com;persist security info=False;initial catalog=portafolio;TrustServerCertificate=True
     ```
   - Reemplazar `usuario` y `contraseña` con tus credenciales de Somee.

## Configuración de la base de datos

### Configuración local (SQLite)

Por defecto, la aplicación usará SQLite en desarrollo. No se requiere configuración adicional.

### Configuración para producción (SQL Server en Somee)

1. Asegúrate de tener instalado el ODBC Driver 17 for SQL Server.
2. Configura la variable de entorno `SOMEE_CONNECTION_STRING` con tu cadena de conexión de Somee.
3. La aplicación detectará automáticamente el entorno y usará la configuración apropiada.

## Pruebas

### Probar la conexión a la base de datos

```bash
python check_db.py
```

### Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

## Despliegue en Render

1. Crear una nueva aplicación web en Render
2. Conectar el repositorio de GitHub
3. Configurar las variables de entorno en el panel de Render:
   - `SOMEE_CONNECTION_STRING`: Tu cadena de conexión de Somee
   - `PYTHON_VERSION`: 3.8.0 o superior
   - `DISABLE_COLLECTSTATIC`: 1
4. Configurar el comando de inicio:
   ```
   ./startup.sh
   ```
5. Desplegar la aplicación

## Estructura del proyecto

```
API-Portafolio/
├── api/                    # Aplicación principal de la API
│   ├── migrations/         # Migraciones de la base de datos
│   ├── __init__.py
│   ├── admin.py            # Configuración del admin de Django
│   ├── apps.py             # Configuración de la aplicación
│   ├── models.py           # Modelos de la base de datos
│   ├── serializers.py      # Serializadores de la API
│   ├── tests.py            # Pruebas unitarias
│   └── views.py            # Vistas de la API
├── core/                   # Configuración principal del proyecto
│   ├── __init__.py
│   ├── asgi.py             # Configuración ASGI
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
├── static/                 # Archivos estáticos
├── .env.example           # Ejemplo de archivo .env
├── .gitignore             # Archivos ignorados por Git
├── Dockerfile             # Configuración de Docker
├── manage.py              # Script de gestión de Django
├── requirements.txt       # Dependencias de Python
└── startup.sh             # Script de inicio para producción
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
