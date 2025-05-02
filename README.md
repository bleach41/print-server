# Servidor de Impresión

Este es un servidor de impresión desarrollado en Python que permite imprimir códigos QR y texto a través de una API REST.

## Características

- API REST para imprimir códigos QR y texto
- Soporte para impresoras térmicas Munbyn
- Verificación de estado de impresora
- Listado de impresoras disponibles
- CORS habilitado para integración con aplicaciones web
- Ejecutable Windows para instalación simple

## Requisitos

### Para instalación directa:
- Python 3.x
- Windows (debido al uso de win32print)
- Impresora térmica Munbyn compatible

### Para el ejecutable:
- Windows 10/11
- Impresora térmica Munbyn compatible instalada

## Instalación

### Usando el Ejecutable (Método recomendado):

1. Descargar el archivo `app.exe` de la carpeta `dist`
2. Hacer doble clic en el ejecutable
3. El servidor se iniciará automáticamente en http://localhost:3001

### Instalación Manual (Para desarrolladores):

1. Clonar el repositorio:
```bash
git clone origin https://github.com/bleach41/print-server 
cd print-server/python
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Iniciar el servidor:
```bash
python src/server/app.py
```

## Construir el Ejecutable (Para desarrolladores)

Para generar un nuevo ejecutable:

1. Instalar dependencias de desarrollo:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

2. Ejecutar el script de construcción:
```bash
python build.py
```

El ejecutable se generará automáticamente en la carpeta `dist`.

## API Endpoints

### POST /print
Envía código para imprimir

Ejemplo de solicitud:
```json
{
    "code": "ABC123",
    "productId": "78954",
    "customer": "Juan Pérez",
    "total": "125.00",
    "notes": "Notas adicionales"
}
```

Respuesta exitosa:
```json
{
    "success": true,
    "message": "Código ABC123 enviado a imprimir con QR"
}
```

### GET /status
Verifica el estado de la impresora

Respuesta exitosa:
```json
{
    "status": "ready",
    "message": "Impresora conectada y lista"
}
```

### GET /printers
Lista las impresoras disponibles

Respuesta exitosa:
```json
{
    "success": true,
    "printers": [
        {
            "name": "Munbyn Printer",
            "port": "USB001",
            "driver": "Generic / Text Only"
        }
    ]
}
```

## Estructura del Proyecto

```
python/
├── src/
│   ├── server/
│   │   └── app.py      # Servidor principal
│   └── printer/
│       └── printer.py   # Módulo de impresión
├── build.py            # Script de construcción
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Documentación
```

## Notas importantes

1. El ejecutable debe ejecutarse con permisos de administrador la primera vez
2. Se recomienda agregar el ejecutable a las excepciones del antivirus
3. El servidor se iniciará automáticamente al ejecutar el programa
4. Para detener el servidor, cerrar la ventana del programa
5. Los mensajes de estado y errores se mostrarán en la consola
6. La impresora Munbyn debe estar instalada y configurada en Windows antes de ejecutar el programa 