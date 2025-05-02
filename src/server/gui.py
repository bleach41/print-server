import flask.cli
import logging
import os
import threading
import win32print
from datetime import datetime
from flask import Flask
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import psutil
import json

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
        self.print_history = []
        self.history_file = os.path.join(log_dir, 'print_history.json')
        self.load_print_history()
        self.init_ui()
        self.start_flask()

    def init_ui(self):
        self.root.title('Servidor de Impresión')
        self.root.geometry('600x500')

        # Estilo
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        title = ttk.Label(main_frame, text='Servidor de Impresión',
                          font=('Helvetica', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Estado del servidor
        self.status_label = ttk.Label(main_frame, text='Estado: Iniciando...')
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Notebook para pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=2,
                      sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Pestaña de Control
        control_frame = ttk.Frame(notebook, padding="5")
        notebook.add(control_frame, text='Control')

        # Botones en la pestaña de Control
        self.status_btn = ttk.Button(
            control_frame, text='Verificar Estado', command=self.check_printer_status)
        self.status_btn.pack(fill=tk.X, pady=2)

        self.printers_btn = ttk.Button(
            control_frame, text='Listar Impresoras', command=self.show_printers)
        self.printers_btn.pack(fill=tk.X, pady=2)

        self.logs_btn = ttk.Button(
            control_frame, text='Abrir Logs', command=self.open_logs)
        self.logs_btn.pack(fill=tk.X, pady=2)

        self.restart_btn = ttk.Button(
            control_frame, text='Reiniciar Servidor', command=self.restart_server)
        self.restart_btn.pack(fill=tk.X, pady=2)

        # Pestaña de Estado del Servidor
        server_frame = ttk.Frame(notebook, padding="5")
        notebook.add(server_frame, text='Estado del Servidor')

        # Información del servidor
        self.server_info = scrolledtext.ScrolledText(
            server_frame, height=10, wrap=tk.WORD)
        self.server_info.pack(fill=tk.BOTH, expand=True)

        # Pestaña de Historial
        history_frame = ttk.Frame(notebook, padding="5")
        notebook.add(history_frame, text='Historial')

        # Lista de historial
        self.history_tree = ttk.Treeview(history_frame, columns=(
            'fecha', 'codigo', 'estado'), show='headings')
        self.history_tree.heading('fecha', text='Fecha')
        self.history_tree.heading('codigo', text='Código')
        self.history_tree.heading('estado', text='Estado')
        self.history_tree.column('fecha', width=150)
        self.history_tree.column('codigo', width=200)
        self.history_tree.column('estado', width=100)
        self.history_tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar para el historial
        scrollbar = ttk.Scrollbar(
            history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # Barra de estado
        self.status_bar = ttk.Label(
            main_frame, text='Servidor iniciado en http://localhost:3001')
        self.status_bar.grid(row=3, column=0, columnspan=2, pady=5)

        # Configurar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Timer para actualizar el estado
        self.update_status()

    def update_status(self):
        self.check_printer_status()
        self.update_server_info()
        self.root.after(30000, self.update_status)

    def update_server_info(self):
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            cpu_percent = process.cpu_percent()
            uptime = datetime.now() - datetime.fromtimestamp(process.create_time())
            uptime_str = str(uptime).split('.')[0]  # Eliminar microsegundos

            info_text = f"""INFORMACIÓN DEL SERVIDOR
            
• Estado: Activo y ejecutándose
• CPU: {cpu_percent:.1f}%
• Memoria: {memory_info.rss / 1024 / 1024:.1f} MB
• Puerto: 3001
• Tiempo activo: {uptime_str}
• Directorio de logs: {log_dir}

INFORMACIÓN DE RED
• URL: http://localhost:3001
• Protocolo: HTTP
• CORS: Habilitado

INFORMACIÓN DE IMPRESORA"""

            try:
                printers = win32print.EnumPrinters(
                    win32print.PRINTER_ENUM_LOCAL, None, 2)
                printer_found = any(
                    "Munbyn" in printer['pPrinterName'] for printer in printers)
                if printer_found:
                    info_text += "\n• Estado: ✅ Impresora conectada y lista"
                    for printer in printers:
                        if "Munbyn" in printer['pPrinterName']:
                            info_text += f"\n• Nombre: {printer['pPrinterName']}"
                            info_text += f"\n• Puerto: {printer['pPortName']}"
                            info_text += f"\n• Driver: {printer['pDriverName']}"
                else:
                    info_text += "\n• Estado: ❌ Impresora no encontrada"
            except Exception as e:
                info_text += f"\n• Error al obtener información de la impresora: {str(e)}"

            self.server_info.delete(1.0, tk.END)
            self.server_info.insert(tk.END, info_text)

        except Exception as e:
            error_msg = f"Error al actualizar información del servidor: {str(e)}"
            logger.error(error_msg)
            self.server_info.delete(1.0, tk.END)
            self.server_info.insert(tk.END, f"Error: {error_msg}")

    def add_to_history(self, code, status):
        now = datetime.now()
        history_item = {
            'fecha': now.strftime('%Y-%m-%d %H:%M:%S'),
            'codigo': code,
            'estado': status
        }
        self.print_history.append(history_item)
        self.save_print_history()
        self.update_history_display()

        # Actualizar la interfaz inmediatamente
        self.root.update_idletasks()

    def update_history_display(self):
        # Limpiar el árbol
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Agregar elementos del historial en orden inverso (más recientes primero)
        # Mostrar los últimos 100 registros
        for item in reversed(self.print_history[-100:]):
            self.history_tree.insert('', 0, values=(
                item['fecha'],
                item['codigo'],
                item['estado']
            ))

    def load_print_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.print_history = json.load(f)
            else:
                self.print_history = []
                # Crear el archivo si no existe
                self.save_print_history()
        except Exception as e:
            logger.error(f"Error al cargar historial: {str(e)}")
            self.print_history = []

    def save_print_history(self):
        try:
            # Asegurarse de que el directorio existe
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.print_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error al guardar historial: {str(e)}")

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
