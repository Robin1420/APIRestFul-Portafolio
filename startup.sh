#!/bin/bash

# Mostrar información de depuración
echo "=== Iniciando la aplicación ==="
echo "Directorio actual: $(pwd)"
echo "Python version: $(python --version)"

# Mostrar información de ODBC instalado
echo "=== Información de ODBC instalado ==="
odbcinst -j
ls -la /opt/microsoft/msodbcsql17/lib64/

# Verificar si estamos en producción
if [ -n "$RENDER" ]; then
    echo "=== Modo producción (Render) detectado ==="
    
    # Mostrar información de la base de datos (sin contraseña)
    echo "=== Información de la base de datos ==="
    if [ -n "$SOMEE_CONNECTION_STRING" ]; then
        echo "SOMEE_CONNECTION_STRING está configurada"
        # Mostrar la cadena de conexión sin la contraseña
        echo "Cadena de conexión: ${SOMEE_CONNECTION_STRING/pwd=*;/pwd=******;}"
        
        # Crear un script de prueba de conexión
        cat > /tmp/test_connection.py << 'EOL'
import os
import pyodbc

print("=== Información del sistema ===")
print(f"Versión de pyodbc: {pyodbc.version}")
print("\n=== Drivers ODBC disponibles ===")
for driver in pyodbc.drivers():
    print(f"- {driver}")

print("\n=== Fuentes de datos ===")
for source in pyodbc.dataSources():
    print(f"- {source}: {pyodbc.dataSources()[source]}")

print("\n=== Intentando conectar con la cadena de conexión ===")
conn_str = os.environ['SOMEE_CONNECTION_STRING']
print(f"Cadena de conexión: {conn_str.replace('pwd=*;', 'pwd=******;')}")

try:
    print("\n=== Estableciendo conexión... ===")
    conn = pyodbc.connect(conn_str, timeout=10)
    cursor = conn.cursor()
    print("Conexión exitosa!")
    
    print("\n=== Probando consulta simple... ===")
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"Resultado de la consulta: {result[0]}")
    
    print("\n=== Listando tablas disponibles... ===")
    cursor.tables()
    tables = cursor.fetchall()
    print(f"Tablas encontradas: {len(tables)}")
    for table in tables[:5]:  # Mostrar solo las primeras 5 tablas
        print(f"- {table.table_name} ({table.table_type})")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"\n=== Error al conectar a la base de datos ===")
    print(f"Tipo de error: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    if hasattr(e, 'args') and len(e.args) > 0:
        print("\nArgumentos del error:")
        for i, arg in enumerate(e.args):
            print(f"  {i+1}. {arg}")
    raise SystemExit(1)
EOL

        echo "=== Probando conexión a la base de datos SQL Server ==="
        if python /tmp/test_connection.py; then
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