# PASO 1:
# Instalamos la version de python que queremos, en este caso 3.11
FROM python:3.11-slim

# Buenas practicas: Establecer variables de entorno 
# le dicen a python que no genere archivos .pyc y que muestre los print inmediatamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# PASO 2:
# Crear el directorio de trabajo
# aqui creas y te mueves a la carpeta /app dentro del contenedor
# Todo lo que hagas a partir de aqui se hara dentro de /app
WORKDIR /app

# PASO 3:
# Copiar e instalar las dependencias
# Primero copias SOLO el archivo requirements.txt, el . indica que es el directorio actual
COPY requirements.txt . 
# Luego, ejecutas pip install. Docker guardara esta capa en cache.
RUN pip install -r requirements.txt

# PASO 4:
# Copiar todo tu codigo, Ahora que las dependencias (que rara vez cambian) estan instaladas,
# copias el resto de tu codigo fuente al contenedor.
# Los .. indican que se copian todos los archivos y carpetas del directorio actual al contenedor
COPY . .

# PASO 5:
# (Opcional pero recomendado): Exponer el puerto.
# Esto es como una documentacion para Docker y para otros desarrolladores.
# Informa que la aplicacion dentro del contenedor usara el puerto 8000.
EXPOSE 8000

# PASO 6:
# Comando para ejecutar tu aplicacion
# Este es el comando que se ejecutara cuando inicies el contenedor.
# Usamos 0.0.0.0 para que el servidor sea accesible desde fuera del contenedor.
CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]