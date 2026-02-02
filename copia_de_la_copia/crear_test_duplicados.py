# Script de Prueba - Crear archivos duplicados de ejemplo

import os
import shutil

# Crear carpeta de prueba
test_folder = r"C:\Users\ernes\Desktop\proyectofinal\test_duplicados"
if os.path.exists(test_folder):
    shutil.rmtree(test_folder)
os.makedirs(test_folder)

# Crear archivos originales
files = {
    "documento1.txt": "Contenido del documento 1\nEsto es texto de prueba",
    "imagen.txt": "Este archivo simula una imagen\nContenido único de imagen",
    "datos.csv": "nombre,edad,ciudad\nJuan,25,Madrid\nMaria,30,Barcelona",
}

for filename, content in files.items():
    with open(os.path.join(test_folder, filename), "w", encoding="utf-8") as f:
        f.write(content)

# Crear duplicados (copias exactas)
for filename in files.keys():
    # Crear 2 duplicados de cada archivo
    base, ext = os.path.splitext(filename)
    for i in range(1, 3):
        dup_name = f"{base}_copia{i}{ext}"
        shutil.copy2(
            os.path.join(test_folder, filename),
            os.path.join(test_folder, dup_name)
        )

print(f"✅ Carpeta de prueba creada: {test_folder}")
print(f"📁 Total de archivos: {len(os.listdir(test_folder))}")
print(f"   - 3 archivos originales")
print(f"   - 6 archivos duplicados")
print()
print("🎯 Ahora puedes:")
print("1. Ejecutar la app: python app.py")
print("2. Pulsar 'Seleccionar carpeta'")
print(f"3. Elegir: {test_folder}")
print("4. Ver los 6 duplicados detectados")
print("5. Probar eliminar individual o grupal")
