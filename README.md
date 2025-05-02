# Servidor de Impresión

Este es un servidor de impresión desarrollado en Python que permite imprimir códigos QR y texto a través de una API REST.

## Características

- API REST para imprimir códigos QR
- Soporte para impresoras térmicas
- Verificación de estado de impresora
- Listado de impresoras disponibles
- CORS habilitado para integración con aplicaciones web
- Contenedor Docker para fácil despliegue

## Requisitos

### Para instalación directa:
- Python 3.x
- Windows (debido al uso de win32print)
- Impresora térmica compatible

### Para instalación con Docker:
- Windows 10/11 o Windows Server con:
  - Docker Desktop instalado
  - WSL 2 habilitado
  - Impresora térmica compatible instalada en Windows

## Instalación

### Usando Docker (Recomendado):

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd print-server
```

2. Construir y ejecutar con Docker Compose:
```bash
docker-compose up -d
```

El servidor estará disponible en http://localhost:3001

### Instalación Manual:

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd print-server
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Iniciar el servidor:
```bash
python src/server/app.py
```

## Endpoints

- `POST /print`: Envía código para imprimir
- `GET /status`: Verifica el estado de la impresora
- `GET /printers`: Lista las impresoras disponibles

## Estructura del Proyecto

```
python/
├── src/
│   ├── server/
│   │   └── app.py
│   └── printer/
│       └── printer.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Notas importantes para Docker

1. El contenedor necesita acceso a las impresoras del sistema host
2. Asegúrate de que la impresora esté instalada y funcionando en Windows antes de iniciar el contenedor
3. El contenedor se reiniciará automáticamente en caso de fallos
4. Para ver los logs del contenedor:
```bash
docker-compose logs -f
``` 