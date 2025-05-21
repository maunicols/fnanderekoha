# Usa una imagen base oficial de Python en Alpine Linux
FROM python:3.9-alpine

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=fundacionnanderekoha.settings

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev

# Copia requirements e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Crea y configura el usuario no root
RUN adduser -D appuser && \
    chown -R appuser:appuser /app

# Cambia al usuario no root
USER appuser

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto
EXPOSE 8000

# Define el comando por defecto
CMD ["gunicorn", "fundacionnanderekoha.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
