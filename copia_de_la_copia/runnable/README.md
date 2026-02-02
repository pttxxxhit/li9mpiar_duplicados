# Copia runnable

Esta carpeta contiene una copia mínima del proyecto lista para ejecutar con Python + Flet.

Instrucciones rápidas (Windows PowerShell):

1. Crear y activar un entorno virtual (opcional pero recomendado):

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

2. Instalar dependencias:

   python -m pip install -r requirements.txt

3. Ejecutar la app minimal:

   python main_minimal.py

Archivos incluidos:
- main_minimal.py
- borrar_duplicados.py
- requirements.txt
- run_minimal.bat
- run_tests_borrar_duplicados.py
- assets/ (carpeta con fondo y otros assets necesarios)

Para convertir en un exe posteriormente puedes usar PyInstaller o similar.
