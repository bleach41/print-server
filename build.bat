@echo off
cd /d "%~dp0"
echo Directorio actual: %CD%

echo Verificando archivos necesarios...
if not exist "requirements.txt" (
    echo ERROR: No se encuentra requirements.txt
    pause
    exit /b 1
)

if not exist "src\server\app.py" (
    echo ERROR: No se encuentra app.py
    pause
    exit /b 1
)

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Construyendo ejecutable...
pyinstaller ^
    src/server/app.py ^
    --name=PrintServer ^
    --onefile ^
    --noconsole ^
    --add-data="src/printer;printer" ^
    --hidden-import=win32print ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=tkinter ^
    --clean ^
    --windowed

echo.
echo Verificando carpeta dist...
if exist "dist" (
    echo Carpeta dist encontrada
    dir dist
) else (
    echo ERROR: Carpeta dist no encontrada
)

echo.
echo Limpiando archivos temporales...
rmdir /s /q build 2>nul
rmdir /s /q __pycache__ 2>nul

echo.
echo Proceso completado
pause 