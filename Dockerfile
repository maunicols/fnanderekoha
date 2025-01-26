# Usa una imagen base oficial de Python en Alpine Linux
FROM python:3.9-alpine

# Instala las dependencias del sistema
RUN apk add --no-cache gcc musl-dev libffi-dev

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic

# Copia todo el contenido de la carpeta raíz del proyecto al directorio de trabajo
COPY . .

# Expone el puerto en el que correrá la aplicación Django
EXPOSE 8000

# Define el comando por defecto para correr la aplicación
CMD ["gunicorn", "fundacionnanderekoha.wsgi", "-p", "0.0.0.0:8000"]
