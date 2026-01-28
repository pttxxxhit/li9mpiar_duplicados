#!/usr/bin/env python3
"""
Script de prueba para verificar que los duplicados se encuentran y se pueden eliminar
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from borrar_duplicados import find_duplicates, delete_file

# Crear directorio de prueba
test_dir = "test_app_fix"

print("=" * 60)
print("PRUEBA DE ELIMINACIÓN DE DUPLICADOS")
print("=" * 60)

# Verificar archivos duplicados
if os.path.exists(test_dir):
    print(f"\n✓ Directorio de prueba encontrado: {test_dir}")

    # Buscar duplicados
    print("\n🔍 Buscando duplicados...")
    duplicates = find_duplicates(test_dir)

    if duplicates:
        print(f"\n✅ Se encontraron {len(duplicates)} archivos duplicados:")
        for idx, (dup, orig) in enumerate(duplicates, 1):
            print(f"\n  {idx}. Duplicado: {os.path.basename(dup)}")
            print(f"     Ruta: {dup}")
            print(f"     Original: {os.path.basename(orig)}")
            print(f"     Ruta: {orig}")

        # Intentar eliminar el primer duplicado
        print(f"\n🗑️  Intentando eliminar el primer duplicado...")
        dup_to_delete = duplicates[0][0]

        if delete_file(dup_to_delete):
            print(f"  ✅ Eliminado exitosamente: {os.path.basename(dup_to_delete)}")
        else:
            print(f"  ❌ Error al eliminar: {os.path.basename(dup_to_delete)}")

        # Verificar duplicados restantes
        print("\n🔍 Buscando duplicados nuevamente...")
        remaining_dups = find_duplicates(test_dir)
        if remaining_dups:
            print(f"✅ Se encontraron {len(remaining_dups)} duplicados restantes")
        else:
            print(f"✅ No hay más duplicados en la carpeta")
    else:
        print("\n⚠️  No se encontraron duplicados en la carpeta")
        print("\nLista de archivos en la carpeta:")
        for f in os.listdir(test_dir):
            print(f"  - {f}")
else:
    print(f"\n❌ Directorio de prueba no encontrado: {test_dir}")

print("\n" + "=" * 60)
print("FIN DE LA PRUEBA")
print("=" * 60)
