import flask.cli
import pystray
import PIL.Image
import io
import logging
import os
import threading
from datetime import datetime
from flask import Flask

# Configurar logging
log_dir = os.path.join(os.path.expanduser("~"), "PrintServer", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(
    log_dir, f"print_server_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8')
        # Removemos el StreamHandler para que no escriba en consola
    ]
)

# Configurar Flask para que no muestre mensajes en consola
flask.cli.show_server_banner = lambda *args: None
logging.getLogger('werkzeug').disabled = True

logger = logging.getLogger(__name__)


class PrintServerGUI:
    def __init__(self, app: Flask):
        self.app = app
        self.server_thread = None
        self.icon = None
        self.create_icon()

    def create_icon(self):
        # Crear un ícono simple (un círculo blanco)
        image = PIL.Image.new('RGB', (64, 64), 'black')
        dc = PIL.ImageDraw.Draw(image)
        dc.ellipse([16, 16, 48, 48], fill='white')

        self.icon = pystray.Icon(
            "print_server",
            image,
            "Servidor de Impresión",
            menu=self.create_menu()
        )

    def create_menu(self):
        return pystray.Menu(
            pystray.MenuItem(
                "Estado",
                self.show_status,
                default=True  # Este será el ítem por defecto al hacer doble clic
            ),
            pystray.MenuItem(
                "Ver logs",
                self.open_logs
            ),
            pystray.MenuItem(
                "Reiniciar servidor",
                self.restart_server
            ),
            pystray.MenuItem(
                "Salir",
                self.stop_server
            )
        )

    def show_status(self, icon, item):
        import win32print
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL, None, 2)
            printer_found = any(
                "Munbyn" in printer['pPrinterName'] for printer in printers)
            status = "Impresora conectada y lista" if printer_found else "Impresora no encontrada"
            self.icon.notify(status)
            logger.info(f"Estado del servidor: {status}")
        except Exception as e:
            error_msg = f"Error al verificar estado: {str(e)}"
            self.icon.notify(error_msg)
            logger.error(error_msg)

    def open_logs(self, icon, item):
        try:
            os.startfile(log_dir)
            logger.info("Abriendo directorio de logs")
        except Exception as e:
            error_msg = f"Error al abrir logs: {str(e)}"
            self.icon.notify(error_msg)
            logger.error(error_msg)

    def restart_server(self, icon, item):
        logger.info("Reiniciando servidor...")
        self.stop_flask()
        self.start_flask()
        self.icon.notify("Servidor reiniciado")

    def stop_server(self, icon, item):
        logger.info("Deteniendo servidor...")
        self.stop_flask()
        icon.stop()

    def start_flask(self):
        def run_server():
            try:
                self.app.run(host='0.0.0.0', port=3001)
            except Exception as e:
                logger.error(f"Error en el servidor: {str(e)}")
                self.icon.notify(
                    "Error en el servidor. Revise los logs para más detalles.")

        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        logger.info("Servidor iniciado en http://localhost:3001")

    def stop_flask(self):
        if self.server_thread and self.server_thread.is_alive():
            import requests
            try:
                requests.get('http://localhost:3001/shutdown')
            except:
                pass
            self.server_thread = None

    def run(self):
        self.start_flask()
        logger.info("Iniciando interfaz gráfica")
        self.icon.run()
