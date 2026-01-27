# Proyecto Automatización de Tareas (Flet)

Este proyecto incluye una interfaz Flet para:
- Detectar y eliminar archivos duplicados en una carpeta.
- Organizar archivos por tipo (extensión) en subcarpetas.

## Requisitos
- Windows con PowerShell.
- Python 3.11+ (usa el entorno virtual incluido: `.venv`).
- Flet 0.80+ (versión moderna instalada).

## Instalación

Usa el intérprete del entorno virtual incluido para instalar dependencias:

```powershell
C:\Users\ernes\Desktop\proyectofinal\.venv\Scripts\python.exe -m pip install --upgrade pip
C:\Users\ernes\Desktop\proyectofinal\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecutar

- App básica (2 vistas: Duplicados y Organizar):
```powershell
C:\Users\ernes\Desktop\proyectofinal\.venv\Scripts\python.exe app.py
```

- App extendida con fondo opcional (si existe `assets/fondo.jpg`):
```powershell
C:\Users\ernes\Desktop\proyectofinal\.venv\Scripts\python.exe main.py
```

## Uso

- Duplicados:
  1. Pulsa "Seleccionar carpeta".
  2. La lista mostrará los duplicados (si hay). Puedes eliminar individuales o todos.

- Organizar:
  1. Pulsa "Seleccionar carpeta".
  2. Pulsa "Organizar" para mover archivos a subcarpetas: Imagenes, Videos, Documentos, Datasets, Comprimidos, Otros.

## Notas
- El proyecto usa Flet 0.80+ (versión moderna con todas las características).
- Si el editor marca "No module named 'flet'", asegúrate de estar usando el intérprete de `.venv`.
- Las demás vistas (Redimensionar, Convertir, Extraer audio, Fusionar PDFs, Renombrar) requieren módulos que no están presentes aún.


