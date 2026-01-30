=====================================
AUTOMATIZACIÓN DE TAREAS - README
=====================================

DESCRIPCIÓN:
Aplicación de escritorio para automatizar tareas comunes con archivos.

FUNCIONALIDADES:
1. Eliminar Duplicados - Encuentra y elimina archivos duplicados por hash SHA256
2. Organizar Archivos - Organiza archivos por tipo (imágenes, videos, documentos, etc.)
3. Redimensionar - Cambia el tamaño de imágenes individuales

REQUISITOS:
- Python 3.9 o superior
- Dependencias en requirements.txt

INSTALACIÓN:
1. Instalar dependencias:
   pip install -r requirements.txt

2. Ejecutar la aplicación:
   python main.py

USO:

ELIMINAR DUPLICADOS:
- Selecciona una carpeta
- Marca los duplicados con checkboxes
- Usa "Seleccionar todos" o "Deseleccionar todos"
- Haz clic en "ELIMINAR X SELECCIONADOS"
- Los archivos se eliminan sin confirmación adicional

ORGANIZAR ARCHIVOS:
- Selecciona carpeta a organizar
- Haz clic en "Organizar"
- Los archivos se mueven a subcarpetas por tipo

REDIMENSIONAR IMAGEN:
- Haz clic en "Seleccionar archivo"
- Elige imagen (JPG, PNG, BMP, GIF, TIFF, WEBP)
- Selecciona carpeta de salida
- Ingresa ancho y alto en píxeles
- Haz clic en "Redimensionar"
- El archivo se guarda como nombre_resized.ext

NOTAS:
- La eliminación de duplicados es permanente
- Los botones individuales rojos eliminan archivos uno por uno
- El redimensionamiento mantiene el formato original
- La app usa tema oscuro con fondo translúcido

SOPORTE:
GitHub: https://github.com/pttxxxhit/automatizacion-tareas

Fecha: 30 Enero 2026
