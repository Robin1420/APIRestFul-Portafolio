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
        
        # Verificar si podemos conectarnos a la base de datos
        echo "=== Probando conexión a la base de datos SQL Server ==="
        if python -c "
import os, pyodbc
conn_str = os.environ['SOMEE_CONNECTION_STRING']
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    print('Conexión exitosa a SQL Server')
except Exception as e:
    print(f'Error al conectar a SQL Server: {str(e)}')
    raise SystemExit(1)
"; then
            echo "=== La conexión a la base de datos fue exitosa ==="
            echo "=== Aplicando migraciones a la base de datos SQL Server ==="
            python manage.py migrate --noinput || echo "ADVERTENCIA: Error al aplicar migraciones"
        else
            echo "=== No se pudo conectar a la base de datos SQL Server ==="
            exit 1
        fi
    else
        echo "=== ERROR: SOMEE_CONNECTION_STRING no está configurada ==="
        exit 1
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
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --log-level=debug --access-logfile - --error-logfile -