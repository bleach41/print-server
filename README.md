# Servidor de Impresión

Este es un servidor de impresión desarrollado en Python que permite imprimir códigos QR y texto a través de una API REST.

## Características

- API REST para imprimir códigos QR y texto
- Soporte para impresoras térmicas Munbyn
- Verificación de estado de impresora
- Listado de impresoras disponibles
- CORS habilitado para integración con aplicaciones web
- Instalador Windows profesional
- Inicio automático con Windows (opcional)

## Requisitos

### Para usuarios finales:
- Windows 10/11
- Impresora térmica Munbyn compatible instalada

### Para desarrolladores:
- Python 3.x
- Windows (debido al uso de win32print)
- NSIS (para crear el instalador)

## Instalación

### Para Usuarios Finales:

1. Descargar `PrintServer-Setup.exe`
2. Ejecutar el instalador
3. Seguir las instrucciones en pantalla
4. La aplicación se iniciará automáticamente al finalizar la instalación

El programa se instalará en:
- Programa: `C:\Program Files\TECOPOS\Print Server\`
- Acceso directo: Escritorio y Menú Inicio
- Inicio automático con Windows (opcional)

Para desinstalar:
1. Ir a "Agregar o quitar programas"
2. Buscar "Print Server"
3. Hacer clic en "Desinstalar"

### Para Desarrolladores:

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

## Construir el Instalador (Para desarrolladores)

1. Instalar dependencias de desarrollo:
```bash
pip install -r requirements.txt
pip install pyinstaller
winget install NSIS.NSIS
```

2. Generar el ejecutable:
```bash
python build.py
```

3. Crear el instalador:
```bash
makensis installer.nsi
```

El instalador `PrintServer-Setup.exe` se generará en el directorio actual.

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