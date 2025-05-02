import os
import sys
import traceback
import logging
from datetime import datetime

try:
    import win32print
    import time
    from flask_cors import CORS
    from flask import Flask, request, jsonify
    import qrcode
    from PIL import Image, ImageWin, ImageFont, ImageDraw
    import win32ui
    import win32con
    import win32gui
    from gui import PrintServerGUI, logger
    print("Todas las dependencias importadas correctamente")
except ImportError as e:
    print(f"Error al importar dependencias: {str(e)}")
    print("Traceback completo:")
    traceback.print_exc()
    input("Presione Enter para salir...")
    sys.exit(1)

# Asegurarnos de que el directorio src esté en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

logger.info("Directorio actual: %s", os.getcwd())
logger.info("Directorio src: %s", src_dir)
logger.info("Python path: %s", sys.path)

# Importar el módulo printer
try:
    from printer.printer import test_direct_print
    logger.info("Módulo printer importado correctamente")
except ImportError as e:
    logger.error("Error: No se pudo importar el módulo printer - %s", str(e))
    logger.error("Traceback completo:")
    traceback.print_exc()
    input("Presione Enter para salir...")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Variable global para la interfaz gráfica
gui = None

logger.info("Iniciando servidor de impresión...")
logger.info("El servidor estará disponible en: http://localhost:3001")


@app.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('No se ejecuta con el servidor de desarrollo')
    func()
    return 'Servidor detenido...'


@app.route('/print', methods=['POST'])
def print_code():
    try:
        data = request.get_json()
        logger.info("Solicitud de impresión recibida: %s",
                    data.get('code', ''))

        if not data or 'code' not in data:
            logger.error("Error: No se proporcionó el código")
            return jsonify({'error': 'No se proporcionó el código'}), 400

        code = data['code']
        additional_info = ""
        if 'productId' in data:
            additional_info += f"Producto ID: {data['productId']}\n"
        if 'customer' in data:
            additional_info += f"Cliente: {data['customer']}\n"
        if 'total' in data:
            additional_info += f"Total: ${data['total']}\n"
        if 'notes' in data and data['notes']:
            additional_info += f"{data['notes']}\n"

        text_to_print = f"""CÓDIGO: {code}
{additional_info}"""

        logger.info("Enviando a imprimir...")
        success = test_direct_print(text_to_print)

        if success:
            logger.info("Impresión exitosa: %s", code)
            # Registrar en el historial
            if gui and hasattr(gui, 'add_to_history'):
                gui.add_to_history(code, "✅ Exitoso")
            return jsonify({
                'success': True,
                'message': f'Código {code} enviado a imprimir con QR'
            })
        else:
            logger.error("Error durante la impresión")
            # Registrar error en el historial
            if gui and hasattr(gui, 'add_to_history'):
                gui.add_to_history(code, "❌ Error")
            return jsonify({'error': 'Error al imprimir'}), 500

    except Exception as e:
        error_msg = f"Error al imprimir: {str(e)}"
        logger.error(error_msg)
        # Registrar error en el historial
        if gui and hasattr(gui, 'add_to_history'):
            gui.add_to_history(data.get('code', 'N/A'), f"❌ {str(e)}")
        return jsonify({'error': error_msg}), 500


@app.route('/status', methods=['GET'])
def printer_status():
    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL, None, 2)
        printer_found = any(
            "Munbyn" in printer['pPrinterName'] for printer in printers)

        if printer_found:
            logger.info("Verificación de estado: Impresora conectada")
            return jsonify({'status': 'ready', 'message': 'Impresora conectada y lista'})
        else:
            logger.warning("Verificación de estado: Impresora no encontrada")
            return jsonify({'status': 'error', 'message': 'Impresora no encontrada'}), 404

    except Exception as e:
        error_msg = f"Error al verificar estado: {str(e)}"
        logger.error(error_msg)
        return jsonify({'status': 'error', 'message': error_msg}), 500


@app.route('/printers', methods=['GET'])
def list_printers():
    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL, None, 2)
        printer_list = []

        for printer in printers:
            printer_info = {
                'name': printer['pPrinterName'],
                'port': printer['pPortName'],
                'driver': printer['pDriverName']
            }
            printer_list.append(printer_info)
            logger.info("Impresora encontrada: %s", printer['pPrinterName'])

        return jsonify({
            'success': True,
            'printers': printer_list
        })

    except Exception as e:
        error_msg = f"Error al listar impresoras: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500


if __name__ == '__main__':
    try:
        app = Flask(__name__)
        CORS(app)

        # Crear y mostrar la ventana principal
        gui = PrintServerGUI(app)
        gui.run()
    except Exception as e:
        logger.error("Error al iniciar el servidor:")
        logger.error(str(e))
        logger.error("Traceback completo:")
        traceback.print_exc()
        input("Presione Enter para salir...")
