FROM python:3.9-slim

WORKDIR /app

# Variables de entorno para la instalación de ODBC
ENV ACCEPT_EULA=Y
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    unixodbc-utf16 \
    freetds-dev \
    freetds-bin \
    tdsodbc \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Añadir repositorio de Microsoft y claves
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instalar el driver ODBC de Microsoft
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        msodbcsql17 \
        mssql-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Asegurarse de que el driver ODBC esté configurado correctamente
RUN echo "[ODBC Driver 17 for SQL Server]\nDriver = ODBC Driver 17 for SQL Server\n" >> /etc/odbcinst.ini

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Hacer ejecutable el script de inicio
RUN chmod +x /app/startup.sh

# Puerto expuesto
EXPOSE $PORT

# Comando para ejecutar la aplicación
CMD ["./startup.sh"]