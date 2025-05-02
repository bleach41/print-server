import subprocess
import os
import sys

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Directorio de trabajo: {os.getcwd()}")

# Comando de PyInstaller
cmd = [
    'pyinstaller',
    'src/server/app.py',
    '--name=PrintServer',
    '--onefile',
    '--add-data=src/printer;printer',
    '--hidden-import=win32print',
    '--hidden-import=win32gui',
    '--hidden-import=win32api',
    '--hidden-import=win32con',
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--hidden-import=tkinter',
    '--hidden-import=qrcode',
    '--hidden-import=PIL',
    '--hidden-import=PIL._imaging',
    '--hidden-import=PIL.Image',
    '--clean'
]

print("Ejecutando PyInstaller con los siguientes parámetros:")
print(" ".join(cmd))

# Ejecutar PyInstaller
result = subprocess.run(cmd, capture_output=True, text=True)
print("\nSalida de PyInstaller:")
print(result.stdout)
if result.stderr:
    print("\nErrores:")
    print(result.stderr)
