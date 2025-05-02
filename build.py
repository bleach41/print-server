import subprocess
import os
import sys
import shutil

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Directorio de trabajo: {os.getcwd()}")

# Limpiar directorios anteriores
print("Limpiando directorios anteriores...")
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Comando de PyInstaller
cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--name=app",
    "--onefile",
    "--windowed",
    "--add-data=src/printer;printer",
    "--hidden-import=win32print",
    "--hidden-import=win32gui",
    "--hidden-import=win32api",
    "--hidden-import=win32con",
    "--hidden-import=win32ui",
    "--hidden-import=flask",
    "--hidden-import=flask_cors",
    "--hidden-import=qrcode",
    "--hidden-import=PIL",
    "--hidden-import=PIL._imaging",
    "--hidden-import=PIL.Image",
    "--hidden-import=PIL.ImageWin",
    "--hidden-import=PIL.ImageFont",
    "--hidden-import=PIL.ImageDraw",
    "src/server/app.py"
]

print("\nEjecutando PyInstaller con los siguientes parámetros:")
print(" ".join(cmd))

# Ejecutar PyInstaller
result = subprocess.run(cmd, capture_output=True, text=True)
print("\nSalida de PyInstaller:")
print(result.stdout)
if result.stderr:
    print("\nErrores:")
    print(result.stderr)

if result.returncode != 0:
    print("\nError al construir el ejecutable")
    sys.exit(1)
else:
    print("\nEjecutable construido exitosamente")
