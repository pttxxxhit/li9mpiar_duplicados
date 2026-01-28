#!/usr/bin/env python3
"""
Script de prueba para verificar eliminación en paralelo
"""
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))
from borrar_duplicados import find_duplicates, delete_file

test_dir = "test_app_fix"

print("=" * 70)
print("PRUEBA DE ELIMINACIÓN EN PARALELO CON MÚLTIPLES ARCHIVOS")
print("=" * 70)

if os.path.exists(test_dir):
    print(f"\n✓ Directorio de prueba: {test_dir}")

    # Buscar duplicados iniciales
    print("\n🔍 Buscando duplicados...")
    duplicates = find_duplicates(test_dir)

    if duplicates:
        print(f"\n✅ Se encontraron {len(duplicates)} duplicados:")
        to_delete = [dup for dup, _ in duplicates[:3]]  # Tomar los primeros 3

        for idx, dup in enumerate(to_delete, 1):
            print(f"  {idx}. {os.path.basename(dup)}")

        # Simular eliminación paralela (como lo hace la app)
        print(f"\n⏱️  Eliminando {len(to_delete)} archivos en paralelo...")
        start_time = time.time()

        ok = fail = 0
        max_workers = min(8, len(to_delete))

        if len(to_delete) > 1:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(delete_file, dup): dup for dup in to_delete}
                for future in as_completed(futures):
                    try:
                        if future.result():
                            ok += 1
                        else:
                            fail += 1
                    except Exception as ex:
                        print(f"  Error: {ex}")
                        fail += 1
        else:
            for dup in to_delete:
                try:
                    if delete_file(dup):
                        ok += 1
                    else:
                        fail += 1
                except Exception as ex:
                    print(f"  Error: {ex}")
                    fail += 1

        elapsed = time.time() - start_time

        # Resultados
        print(f"\n✅ Eliminación completada en {elapsed:.3f} segundos")
        print(f"   - Eliminados exitosamente: {ok}")
        print(f"   - Errores: {fail}")

        # Verificar duplicados restantes
        print("\n🔍 Buscando duplicados nuevamente...")
        remaining = find_duplicates(test_dir)

        if remaining:
            print(f"✅ Se encontraron {len(remaining)} duplicados restantes")
        else:
            print(f"✅ No hay más duplicados en la carpeta")
    else:
        print("\n⚠️  No hay duplicados para probar")
else:
    print(f"\n❌ Directorio no encontrado: {test_dir}")

print("\n" + "=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)
