#!/bin/bash

# Mostrar información de depuración
echo "=== Iniciando la aplicación ==="
echo "Directorio actual: $(pwd)"
echo "Python version: $(python --version)"

# Verificar si estamos en producción
if [ -n "$RENDER" ]; then
    echo "=== Modo producción (Render) detectado ==="
    
    # Mostrar información de la base de datos (sin contraseña)
    echo "=== Información de la base de datos ==="
    if [ -n "$SOMEE_CONNECTION_STRING" ]; then
        echo "SOMEE_CONNECTION_STRING está configurada"
        # Mostrar la cadena de conexión sin la contraseña
        echo "Cadena de conexión: ${SOMEE_CONNECTION_STRING/pwd=*;/pwd=******;}"
    else
        echo "ADVERTENCIA: SOMEE_CONNECTION_STRING no está configurada"
    fi
    
    # Aplicar migraciones solo si estamos usando SQL Server
    if [ -n "$SOMEE_CONNECTION_STRING" ]; then
        echo "=== Aplicando migraciones a la base de datos SQL Server ==="
        python manage.py migrate --noinput || echo "ADVERTENCIA: Error al aplicar migraciones"
    else
        echo "=== Usando SQLite, omitiendo migraciones ==="
    fi
else
    echo "=== Modo desarrollo detectado ==="
    echo "=== Aplicando migraciones a SQLite ==="
    python manage.py migrate --noinput || echo "ADVERTENCIA: Error al aplicar migraciones"
fi

# Recolectar archivos estáticos
echo "=== Recolectando archivos estáticos ==="
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "=== Iniciando Gunicorn ==="
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --log-level=debug