import win32print
import time
from flask_cors import CORS
from flask import Flask, request, jsonify
import os
import sys

# Asegurarnos de que el directorio src esté en el path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.insert(0, src_dir)

# Importar el módulo printer
try:
    from printer.printer import test_direct_print
except ImportError:
    print("Error: No se pudo importar el módulo printer")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # Esto permite peticiones desde cualquier origen (CORS)


@app.route('/print', methods=['POST'])
def print_code():
    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")

        if not data or 'code' not in data:
            return jsonify({'error': 'No se proporcionó el código'}), 400

        code = data['code']
        print(f"Recibido código para imprimir: {code}")

        # Extraer información adicional si existe
        additional_info = ""
        if 'productId' in data:
            additional_info += f"Producto ID: {data['productId']}\n"
        if 'customer' in data:
            additional_info += f"Cliente: {data['customer']}\n"
        if 'total' in data:
            additional_info += f"Total: ${data['total']}\n"
        if 'notes' in data and data['notes']:
            additional_info += f"{data['notes']}\n"

        # Formatear el texto a imprimir (el código será la primera línea)
        text_to_print = f"""CÓDIGO: {code}
{additional_info}"""
        print(f"Texto formateado para imprimir:\n{text_to_print}")

        # Llamar a la función de impresión
        success = test_direct_print(text_to_print)

        if success:
            return jsonify({
                'success': True,
                'message': f'Código {code} enviado a imprimir con QR'
            })
        else:
            return jsonify({'error': 'Error al imprimir'}), 500

    except Exception as e:
        print(f"Error al imprimir: {str(e)}")
        import traceback
        print("Traceback completo:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/status', methods=['GET'])
def printer_status():
    try:
        # Intentar obtener el nombre de la impresora para verificar si está disponible
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL, None, 2)
        printer_found = any(
            "Munbyn" in printer['pPrinterName'] for printer in printers)

        if printer_found:
            return jsonify({'status': 'ready', 'message': 'Impresora conectada y lista'})
        else:
            return jsonify({'status': 'error', 'message': 'Impresora no encontrada'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


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

        return jsonify({
            'success': True,
            'printers': printer_list
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Servidor de impresión iniciado en el puerto 3001")
    app.run(host='0.0.0.0', port=3001)
