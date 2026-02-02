@echo off
REM Script para ejecutar la versión minimal de la app en Windows (PowerShell por defecto)
python - <<"PY"
import sys
import os
print('Ejecutando main_minimal.py...')
script = os.path.join(os.getcwd(), 'main_minimal.py')
if not os.path.exists(script):
    print('ERROR: main_minimal.py no encontrado en', script)
    sys.exit(1)

os.execv(sys.executable, [sys.executable, script])
PY
