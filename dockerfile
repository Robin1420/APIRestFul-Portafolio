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
    libodbc1 \
    odbcinst1debian2 \
    tdsodbc \
    freetds-dev \
    freetds-bin \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Añadir repositorio de Microsoft y claves
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instalar el driver ODBC de Microsoft
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql17 \
        mssql-tools \
        unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar odbcinst.ini
RUN echo "[ODBC Driver 17 for SQL Server]" >> /etc/odbcinst.ini \
    && echo "Description=Microsoft ODBC Driver 17 for SQL Server" >> /etc/odbcinst.ini \
    && echo "Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.10.so.2.1" >> /etc/odbcinst.ini \
    && echo "UsageCount=1" >> /etc/odbcinst.ini \
    && ln -s /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so /usr/lib/ \
    && ln -s /usr/lib/x86_64-linux-gnu/odbc/odbcinst.ini /etc/odbcinst.ini

# Instalar dependencias de Python
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