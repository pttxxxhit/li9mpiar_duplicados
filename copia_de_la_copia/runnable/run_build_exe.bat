@echo off
REM Script para crear un exe usando PyInstaller (ejecutar desde PowerShell o cmd)
REM Asegúrate de ejecutar este script con privilegios normales; usa un entorno virtual recomendado.

:: 1) Crear/activar virtualenv (si no existe)
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
)

:: 2) Instalar dependencias y PyInstaller
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install pyinstaller

:: 3) Ejecutar PyInstaller (incluye la carpeta assets dentro del exe)
REM --onefile: empaqueta en un solo exe
REM --noconfirm: sobreescribe sin preguntar
REM --add-data "assets;assets" copia la carpeta assets al ejecutable (sintaxis Windows)
.venv\Scripts\pyinstaller --noconfirm --onefile --add-data "assets;assets" --name duplicados main_minimal.py > pyinstaller_build.log 2>&1

:: 4) Mostrar resultado (si existe)
if exist dist\duplicados.exe (
    echo BUILD OK: dist\duplicados.exe
) else (
    echo BUILD FAILED -- revisar pyinstaller_build.log
    type pyinstaller_build.log
)
pause
