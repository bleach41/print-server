# Print Server / Servidor de Impresión

## Español

### Descripción
Servidor de impresión para impresoras térmicas Munbyn, con interfaz gráfica moderna, historial de impresiones y API REST para integración.

### Requisitos
- Windows 10/11
- Impresora térmica Munbyn compatible
- (Para desarrolladores) Python 3.x, NSIS, PyInstaller

### Instalación (Usuarios Finales)
1. Descarga `PrintServer-Setup.exe` (versión 2.0.0)
2. Ejecuta el instalador y sigue las instrucciones
3. El programa se instalará en `C:\Program Files\TECOPOS\Print Server\`
4. Se crearán accesos directos en el escritorio y menú inicio
5. El servidor se iniciará automáticamente con Windows
6. **Los logs e historial se guardan en `%APPDATA%\TECOPOS\PrintServer\logs`** (por ejemplo: `C:\Users\[usuario]\AppData\Roaming\TECOPOS\PrintServer\logs`)

### Desinstalación
- Usa "Agregar o quitar programas" de Windows
- Todos los archivos, logs e historial se eliminarán (haz copia si los necesitas)

### Uso
- La interfaz gráfica permite:
  - Verificar estado de la impresora
  - Listar impresoras
  - Ver y exportar historial (próximamente a Excel)
  - Ver información del servidor
  - Abrir logs
  - Reiniciar el servidor

### API REST
- POST `/print` para imprimir (ver ejemplo más abajo)
- GET `/status` para estado de impresora
- GET `/printers` para listar impresoras

### Ejemplo de solicitud de impresión
```json
{
  "code": "2024100101",
  "productId": "P001",
  "customer": "Juan Pérez",
  "total": 123.45,
  "notes": "Entrega urgente"
}
```

### Desarrollo y construcción del instalador
1. Clona el repositorio
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta: `python build.py`
4. Crea el instalador: `makensis installer.nsi`

---

## English

### Description
Print server for Munbyn thermal printers, with a modern GUI, print history, and REST API for integration.

### Requirements
- Windows 10/11
- Compatible Munbyn thermal printer
- (For developers) Python 3.x, NSIS, PyInstaller

### Installation (End Users)
1. Download `PrintServer-Setup.exe` (version 2.0.0)
2. Run the installer and follow the instructions
3. The program will be installed in `C:\Program Files\TECOPOS\Print Server\`
4. Shortcuts will be created on the desktop and start menu
5. The server will start automatically with Windows
6. **Logs and history are saved in `%APPDATA%\TECOPOS\PrintServer\logs`** (e.g. `C:\Users\[user]\AppData\Roaming\TECOPOS\PrintServer\logs`)

### Uninstallation
- Use Windows "Add or Remove Programs"
- All files, logs, and history will be deleted (make a backup if needed)

### Usage
- The graphical interface allows:
  - Check printer status
  - List printers
  - View and export history (Excel export coming soon)
  - View server information
  - Open logs
  - Restart the server

### REST API
- POST `/print` to print (see example below)
- GET `/status` for printer status
- GET `/printers` to list printers

### Print request example
```json
{
  "code": "2024100101",
  "productId": "P001",
  "customer": "Juan Pérez",
  "total": 123.45,
  "notes": "Urgent delivery"
}
```

### Development and installer build
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python build.py`
4. Create the installer: `makensis installer.nsi`

---

**Contacto / Contact:**
- bleach41
- ftonyalejandrofr@gmail.com 