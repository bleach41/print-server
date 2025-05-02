import os
import traceback

try:
    import win32print
    import qrcode
    import tempfile
    from PIL import Image, ImageWin, ImageFont, ImageDraw
    import win32ui
    import win32con
    import win32gui
    import time
    print("Todas las dependencias importadas correctamente")
except ImportError as e:
    print(f"Error al importar dependencias: {str(e)}")
    print("Traceback completo:")
    traceback.print_exc()
    raise


def generate_qr(data, size=5):
    """Genera un código QR optimizado para papel 2x2 pulgadas."""
    try:
        print(f"\n=== Generando QR ===")
        print(f"Texto para QR: {data}")

        # Crear el objeto QR con tamaño más pequeño para papel 2x2
        qr = qrcode.QRCode(
            version=1,
            # Mayor corrección para impresoras térmicas
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=size,  # Tamaño más pequeño (5 en lugar de 10)
            border=1,       # Borde mínimo
        )
        print("Objeto QR creado")

        # Agregar datos
        qr.add_data(data)
        print("Datos agregados al QR")

        # Generar el QR
        qr.make(fit=True)
        print("QR generado")

        # Crear la imagen
        qr_image = qr.make_image(fill_color="black", back_color="white")
        print("Imagen QR creada")

        # Crear nombre de archivo basado en el código y timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        qr_filename = f"qr_{data}_{timestamp}.png"

        # Obtener la ruta absoluta del directorio del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.dirname(current_dir))
        qr_dir = os.path.join(project_dir, "src", "qr_codes")

        # Asegurarse de que el directorio existe
        os.makedirs(qr_dir, exist_ok=True)

        # Ruta completa del archivo QR
        qr_path = os.path.join(qr_dir, qr_filename)

        # Guardar la imagen
        qr_image.save(qr_path)
        print(f"QR guardado en: {qr_path}")

        # Verificar que el archivo existe y tiene contenido
        if os.path.exists(qr_path):
            file_size = os.path.getsize(qr_path)
            print(f"Archivo QR creado exitosamente. Tamaño: {file_size} bytes")
            if file_size == 0:
                print("¡ADVERTENCIA! El archivo QR está vacío")
                return None
        else:
            print("Error: El archivo QR no se creó correctamente")
            return None

        return qr_path
    except Exception as e:
        print(f"Error al generar QR: {str(e)}")
        import traceback
        print("Traceback completo:")
        traceback.print_exc()
        return None


def create_formatted_ticket(code, additional_info=None):
    """Crea un ticket formateado con código QR y texto para papel 2x2 pulgadas."""
    try:
        print("\n=== Creando ticket formateado ===")

        # Generar el QR primero
        # Tamaño más pequeño para papel 2x2
        qr_path = generate_qr(code, size=5)
        if not qr_path:
            return None

        # Leer la imagen QR
        qr_img = Image.open(qr_path)

        # Crear una nueva imagen blanca del tamaño adecuado para 2x2 pulgadas
        # Asumiendo impresora térmica estándar de 203 DPI, 2 pulgadas = 406 pixels
        width = 384  # Ancho estándar para impresoras térmicas de 2 pulgadas

        # Calcular altura según el contenido
        qr_height = qr_img.height
        text_height = 100  # Espacio estimado para el texto
        padding = 20       # Margen superior e inferior
        height = qr_height + text_height + padding * 2

        # Crear imagen para el ticket completo
        # Modo L (escala de grises 8-bit)
        ticket = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(ticket)

        # Intentar cargar una fuente - si falla, usar default
        try:
            # Intenta cargar fuente monoespaciada de sistema (buenas para tickets)
            font = ImageFont.truetype("consola.ttf", 14)
            small_font = ImageFont.truetype("consola.ttf", 12)
        except IOError:
            # Usar fuente por defecto si no se encuentra
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # Centrar el QR en la imagen
        qr_left = (width - qr_img.width) // 2
        qr_top = padding
        ticket.paste(qr_img, (qr_left, qr_top))

        # Añadir texto debajo del QR
        text_top = qr_top + qr_img.height + 10

        # Centrar el texto del código
        code_text = f"CÓDIGO: {code}"
        code_width = draw.textlength(code_text, font=font)
        draw.text(((width - code_width) // 2, text_top),
                  code_text, font=font, fill=0)

        # Línea divisoria
        draw.line([(20, text_top + 20), (width - 20, text_top + 20)],
                  fill=0, width=1)

        # Fecha/hora debajo de la línea
        date_text = f"Fecha: {time.strftime('%Y-%m-%d %H:%M')}"
        date_width = draw.textlength(date_text, font=small_font)
        draw.text(((width - date_width) // 2, text_top + 25),
                  date_text, font=small_font, fill=0)

        # Información adicional si existe
        if additional_info:
            info_top = text_top + 45
            # Dividir por líneas si es muy largo
            info_lines = additional_info.strip().split('\n')
            for line in info_lines:
                if line.strip():  # Solo procesar líneas no vacías
                    line_width = draw.textlength(line, font=small_font)
                    draw.text(((width - line_width) // 2, info_top),
                              line, font=small_font, fill=0)
                    info_top += 15  # Avanzar a la siguiente línea

        # Guardar el ticket como imagen
        ticket_filename = f"ticket_{code}_{time.strftime('%Y%m%d_%H%M%S')}.png"
        ticket_path = os.path.join(os.path.dirname(qr_path), ticket_filename)
        ticket.save(ticket_path)
        print(f"Ticket creado en: {ticket_path}")

        return ticket_path

    except Exception as e:
        print(f"Error al crear ticket: {str(e)}")
        import traceback
        print("Traceback completo:")
        traceback.print_exc()
        return None


def print_image(image_path, printer_name):
    """Imprime una imagen en la impresora especificada usando GDI."""
    try:
        print(f"\n=== Imprimiendo imagen ===")
        print(f"Ruta de la imagen: {image_path}")

        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            print(f"Error: El archivo {image_path} no existe")
            return False

        # Abrir la imagen con PIL
        img = Image.open(image_path)

        # Convertir a modo 1 (blanco y negro)
        img = img.convert('1')

        # Asegurar que no excede el ancho de la impresora (384 pixels para 2 pulgadas)
        if img.size[0] > 384:
            ratio = 384.0 / img.size[0]
            new_height = int(img.size[1] * ratio)
            img = img.resize((384, new_height))

        print(f"Imagen procesada. Tamaño final: {img.size}")

        # Obtener el contexto de dispositivo de la impresora
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        # Iniciar el documento
        hDC.StartDoc('Ticket')
        hDC.StartPage()

        # Obtener ancho y alto de la imagen
        width, height = img.size

        # Dimensionar en el contexto (escala 1:1)
        dib = ImageWin.Dib(img)
        dib.draw(hDC.GetHandleOutput(), (0, 0, width, height))

        # Finalizar la página y el documento
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()

        print("Impresión GDI de imagen finalizada")

        # Avanzar el papel (opcional)
        handle = win32print.OpenPrinter(printer_name)
        try:
            win32print.StartDocPrinter(
                handle, 1, ("Avance de papel", None, "RAW"))
            try:
                win32print.StartPagePrinter(handle)
                # Enviar avance de papel y corte
                # Avance + comando GS V A para corte parcial
                win32print.WritePrinter(handle, b'\n\n\n\x1D\x56\x41\x00')
                win32print.EndPagePrinter(handle)
            finally:
                win32print.EndDocPrinter(handle)
        finally:
            win32print.ClosePrinter(handle)

        return True

    except Exception as e:
        print(f"Error al imprimir imagen: {str(e)}")
        import traceback
        print("Traceback completo:")
        traceback.print_exc()
        return False


def test_direct_print(text_to_print=None, include_qr=True):
    try:
        print("\n=== Iniciando prueba de impresión ===")

        # Buscar la impresora Munbyn
        printer_name = None
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL, None, 2)
        for printer in printers:
            if "Munbyn" in printer['pPrinterName']:
                printer_name = printer['pPrinterName']
                print(f"\nInformación de la impresora encontrada:")
                print(f"Nombre: {printer['pPrinterName']}")
                print(f"Puerto: {printer['pPortName']}")
                print(f"Driver: {printer['pDriverName']}")
                print(f"Procesador: {printer['pPrintProcessor']}")
                print(f"Tipo de datos: {printer['pDatatype']}")
                break

        if not printer_name:
            print("No se encontró la impresora Munbyn")
            return False

        print(f"\nUsando impresora: {printer_name}")

        # Extraer el código del texto (asumiendo que viene en el formato específico)
        code = None
        additional_info = ""

        if text_to_print:
            lines = text_to_print.split('\n')
            for i, line in enumerate(lines):
                if "CÓDIGO:" in line:
                    code = line.replace("CÓDIGO:", "").strip()
                    # Guardar el resto como información adicional
                    additional_info = '\n'.join(lines[i+1:])
                    break

        # Si no se encontró un código específico, usar un texto genérico
        if not code:
            code = "TEST123"
            print(
                f"No se encontró código en el texto. Usando código genérico: {code}")

        print(f"Código a imprimir: {code}")
        print(f"Información adicional: {additional_info}")

        # Crear un ticket formateado (QR + texto)
        ticket_path = create_formatted_ticket(code, additional_info)
        if not ticket_path:
            print("Error: No se pudo crear el ticket")
            return False

        # Imprimir el ticket
        print(f"Imprimiendo ticket desde: {ticket_path}")
        if print_image(ticket_path, printer_name):
            print("Ticket impreso exitosamente")
            return True
        else:
            print("Error al imprimir el ticket")
            return False

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        print("\nTraceback completo:")
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=== Iniciando prueba de impresión con formato para papel 2x2 pulgadas ===")
    # Prueba con un texto que incluye un código
    test_direct_print("""CÓDIGO: ABC123
Producto ID: 78954
Cliente: Juan Pérez
Total: $125.00""", include_qr=True)
