# Servidor de Impresión

Este es un servidor de impresión desarrollado en Python que permite imprimir códigos QR y texto a través de una API REST.

## Características

- API REST para imprimir códigos QR
- Soporte para impresoras térmicas
- Verificación de estado de impresora
- Listado de impresoras disponibles
- CORS habilitado para integración con aplicaciones web

## Requisitos

- Python 3.x
- Windows (debido al uso de win32print)
- Impresora térmica compatible

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd print-server
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar el servidor:
```bash
python src/server/app.py
```

El servidor se iniciará en el puerto 3001.

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
├── requirements.txt
└── README.md
``` 