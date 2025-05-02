import os
import sys
import traceback

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

print("Directorio actual:", os.getcwd())
print("Directorio src:", src_dir)
print("Python path:", sys.path)

# Importar el módulo printer
try:
    from printer.printer import test_direct_print
    print("Módulo printer importado correctamente")
except ImportError as e:
    print(f"Error: No se pudo importar el módulo printer - {str(e)}")
    print("Traceback completo:")
    traceback.print_exc()
    input("Presione Enter para salir...")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

print("Iniciando servidor de impresión...")
print("El servidor estará disponible en: http://localhost:3001")


@app.route('/print', methods=['POST'])
def print_code():
    try:
        data = request.get_json()
        print(f"Solicitud de impresión recibida: {data.get('code', '')}")

        if not data or 'code' not in data:
            print("Error: No se proporcionó el código")
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

        print("Enviando a imprimir...")
        success = test_direct_print(text_to_print)

        if success:
            print(f"Impresión exitosa: {code}")
            return jsonify({
                'success': True,
                'message': f'Código {code} enviado a imprimir con QR'
            })
        else:
            print("Error durante la impresión")
            return jsonify({'error': 'Error al imprimir'}), 500

    except Exception as e:
        error_msg = f"Error al imprimir: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500


@app.route('/status', methods=['GET'])
def printer_status():
    try:
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL, None, 2)
        printer_found = any(
            "Munbyn" in printer['pPrinterName'] for printer in printers)

        if printer_found:
            print("Verificación de estado: Impresora conectada")
            return jsonify({'status': 'ready', 'message': 'Impresora conectada y lista'})
        else:
            print("Verificación de estado: Impresora no encontrada")
            return jsonify({'status': 'error', 'message': 'Impresora no encontrada'}), 404

    except Exception as e:
        error_msg = f"Error al verificar estado: {str(e)}"
        print(error_msg)
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
            print(f"Impresora encontrada: {printer['pPrinterName']}")

        return jsonify({
            'success': True,
            'printers': printer_list
        })

    except Exception as e:
        error_msg = f"Error al listar impresoras: {str(e)}"
        print(error_msg)
        return jsonify({'error': error_msg}), 500


if __name__ == '__main__':
    try:
        print("Servidor iniciado en http://localhost:3001")
        print("Esperando solicitudes de impresión...")
        app.run(host='0.0.0.0', port=3001)
    except Exception as e:
        print("Error al iniciar el servidor:")
        print(str(e))
        print("Traceback completo:")
        traceback.print_exc()
        input("Presione Enter para salir...")
