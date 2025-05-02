# Usar imagen base de Windows con Python
FROM python:3.11-windowsservercore

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY src/ ./src/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa la aplicación
EXPOSE 3001

# Comando para ejecutar la aplicación
CMD ["python", "src/server/app.py"] 