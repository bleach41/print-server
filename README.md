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

### Usando el Ejecutable (Método más simple):

1. Descargar el archivo `app.exe` de la carpeta `dist`
2. Hacer doble clic en el ejecutable
3. El servidor se iniciará automáticamente en http://localhost:3001

### Instalación Manual:

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
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

## Construir el Ejecutable

Si deseas construir el ejecutable tú mismo:

1. Asegúrate de tener todas las dependencias instaladas:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

2. Ejecutar PyInstaller:
```bash
pyinstaller --onefile --add-data="src/printer;printer" --hidden-import=win32print --hidden-import=win32gui --hidden-import=win32api --hidden-import=win32con --hidden-import=win32ui --hidden-import=flask --hidden-import=flask_cors --hidden-import=qrcode --hidden-import=PIL --hidden-import=PIL._imaging --hidden-import=PIL.Image --hidden-import=PIL.ImageWin --hidden-import=PIL.ImageFont --hidden-import=PIL.ImageDraw src/server/app.py
```

El ejecutable se generará en la carpeta `dist`.

## Endpoints

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

### GET /status
Verifica el estado de la impresora

### GET /printers
Lista las impresoras disponibles

## Estructura del Proyecto

```
python/
├── src/
│   ├── server/
│   │   └── app.py
│   └── printer/
│       └── printer.py
├── build.py
├── requirements.txt
└── README.md
```

## Notas importantes

1. El ejecutable debe ejecutarse con permisos de administrador la primera vez
2. Se recomienda agregar el ejecutable a las excepciones del antivirus
3. El servidor se iniciará automáticamente al ejecutar el programa
4. Para detener el servidor, cerrar la ventana del programa
5. Los mensajes de estado y errores se mostrarán en la consola
6. La impresora Munbyn debe estar instalada y configurada en Windows antes de ejecutar el programa 