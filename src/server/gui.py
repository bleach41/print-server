import flask.cli
import logging
import os
import threading
import win32print
from datetime import datetime
from flask import Flask
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

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
    ]
)

# Configurar Flask para que no muestre mensajes en consola
flask.cli.show_server_banner = lambda *args: None
logging.getLogger('werkzeug').disabled = True

logger = logging.getLogger(__name__)


class PrintServerGUI:
    def __init__(self, app: Flask):
        self.flask_app = app
        self.server_thread = None
        self.root = tk.Tk()
        self.init_ui()
        self.start_flask()

    def init_ui(self):
        self.root.title('Servidor de Impresión')
        self.root.geometry('400x300')

        # Estilo
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        title = ttk.Label(main_frame, text='Servidor de Impresión',
                          font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Estado del servidor
        self.status_label = ttk.Label(main_frame, text='Estado: Iniciando...')
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Botones
        self.status_btn = ttk.Button(
            main_frame, text='Verificar Estado', command=self.check_printer_status)
        self.status_btn.grid(row=2, column=0, columnspan=2,
                             pady=5, sticky=tk.EW)

        self.printers_btn = ttk.Button(
            main_frame, text='Listar Impresoras', command=self.show_printers)
        self.printers_btn.grid(
            row=3, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.logs_btn = ttk.Button(
            main_frame, text='Abrir Logs', command=self.open_logs)
        self.logs_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.restart_btn = ttk.Button(
            main_frame, text='Reiniciar Servidor', command=self.restart_server)
        self.restart_btn.grid(
            row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)

        # Barra de estado
        self.status_bar = ttk.Label(
            main_frame, text='Servidor iniciado en http://localhost:3001')
        self.status_bar.grid(row=6, column=0, columnspan=2, pady=5)

        # Configurar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Timer para actualizar el estado
        self.update_status()

    def update_status(self):
        self.check_printer_status()
        # Actualizar cada 30 segundos
        self.root.after(30000, self.update_status)

    def check_printer_status(self):
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL, None, 2)
            printer_found = any(
                "Munbyn" in printer['pPrinterName'] for printer in printers)

            if printer_found:
                self.status_label.config(
                    text='Estado: ✅ Impresora conectada y lista')
                self.status_bar.config(text='Impresora conectada y lista')
            else:
                self.status_label.config(
                    text='Estado: ❌ Impresora no encontrada')
                self.status_bar.config(text='Impresora no encontrada')

            logger.info(
                f"Estado del servidor verificado: {'conectada' if printer_found else 'no encontrada'}")

        except Exception as e:
            error_msg = f"Error al verificar estado: {str(e)}"
            self.status_label.config(text=f'Estado: ❌ {error_msg}')
            self.status_bar.config(text=error_msg)
            logger.error(error_msg)

    def show_printers(self):
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL, None, 2)
            printer_list = "\n".join(
                [f"• {p['pPrinterName']}" for p in printers])

            # Crear ventana de diálogo
            dialog = tk.Toplevel(self.root)
            dialog.title("Impresoras Disponibles")
            dialog.geometry("300x200")

            # Agregar lista de impresoras
            text = tk.Text(dialog, wrap=tk.WORD)
            text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            text.insert(tk.END, printer_list)
            text.config(state=tk.DISABLED)

            logger.info(f"Listado de impresoras solicitado")
        except Exception as e:
            error_msg = f"Error al listar impresoras: {str(e)}"
            messagebox.showerror("Error", error_msg)
            logger.error(error_msg)

    def open_logs(self):
        try:
            os.startfile(log_dir)
            logger.info("Abriendo directorio de logs")
        except Exception as e:
            error_msg = f"Error al abrir logs: {str(e)}"
            messagebox.showerror("Error", error_msg)
            logger.error(error_msg)

    def restart_server(self):
        logger.info("Reiniciando servidor...")
        self.stop_flask()
        self.start_flask()
        self.status_bar.config(text="Servidor reiniciado correctamente")

    def start_flask(self):
        def run_server():
            try:
                self.flask_app.run(host='0.0.0.0', port=3001)
            except Exception as e:
                logger.error(f"Error en el servidor: {str(e)}")
                self.status_bar.config(text=f"Error en el servidor: {str(e)}")

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

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Está seguro que desea cerrar el servidor?"):
            self.stop_flask()
            self.root.destroy()

    def run(self):
        self.root.mainloop()
