#!/usr/bin/env python3
"""
Script para verificar la conexión a la base de datos SQL Server.
"""
import os
import sys
import pyodbc
from pathlib import Path
from dotenv import load_dotenv

# Configurar logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_environment():
    """Cargar variables de entorno desde .env si existe."""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Cargadas variables de entorno desde: {env_path}")
    else:
        logger.warning(f"No se encontró el archivo .env en: {env_path}")

def test_odbc_drivers():
    """Listar los controladores ODBC disponibles."""
    try:
        drivers = pyodbc.drivers()
        logger.info("Controladores ODBC disponibles:")
        for i, driver in enumerate(drivers, 1):
            logger.info(f"  {i}. {driver}")
        return drivers
    except Exception as e:
        logger.error(f"Error al listar controladores ODBC: {e}")
        return []

def test_connection(connection_string):
    """Probar la conexión a la base de datos."""
    try:
        # Mostrar información de depuración (sin contraseña)
        debug_conn_str = re.sub(r'(pwd|password)=[^;]+', 'pwd=******', connection_string, flags=re.IGNORECASE)
        logger.info(f"Intentando conectar a: {debug_conn_str}")
        
        # Intentar la conexión
        conn = pyodbc.connect(connection_string, timeout=10)
        cursor = conn.cursor()
        
        # Obtener información de la versión de SQL Server
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        logger.info(f"Conexión exitosa a SQL Server: {version}")
        
        # Listar las tablas en la base de datos
        cursor.tables()
        tables = [table.table_name for table in cursor.fetchall() 
                 if table.table_type == 'BASE TABLE' 
                 and table.table_schema == 'dbo']
        logger.info(f"Tablas encontradas ({len(tables)}): {', '.join(tables[:5])}{'...' if len(tables) > 5 else ''}")
        
        # Probar consulta a la tabla de experiencias
        if 'experiencias' in [t.lower() for t in tables]:
            try:
                cursor.execute("SELECT TOP 5 * FROM dbo.experiencias")
                rows = cursor.fetchall()
                logger.info(f"Primeras 5 experiencias: {len(rows)} registros")
                for row in rows:
                    logger.debug(f"  - {row}")
            except Exception as e:
                logger.warning(f"No se pudo consultar la tabla experiencias: {e}")
        
        cursor.close()
        conn.close()
        return True
        
    except pyodbc.Error as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        if hasattr(e, 'args') and len(e.args) > 1:
            logger.error(f"Detalles del error: {e.args[1]}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    import re
    
    # Cargar variables de entorno
    load_environment()
    
    # Obtener la cadena de conexión
    connection_string = os.getenv('SOMEE_CONNECTION_STRING')
    if not connection_string:
        logger.error("Error: La variable de entorno SOMEE_CONNECTION_STRING no está configurada")
        sys.exit(1)
    
    # Verificar controladores ODBC
    drivers = test_odbc_drivers()
    if not drivers:
        logger.warning("No se encontraron controladores ODBC instalados")
    
    # Probar la conexión
    success = test_connection(connection_string)
    
    if success:
        logger.info("Prueba de conexión completada con éxito")
    else:
        logger.error("La prueba de conexión falló")
        sys.exit(1)
