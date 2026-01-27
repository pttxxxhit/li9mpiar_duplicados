import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict


def hash_file(filename, algorithm='sha256'):
    """Hash rápido de archivo usando SHA256 (más rápido que MD5)"""
    h = hashlib.new(algorithm)
    with open(filename, 'rb') as file:
        while chunk := file.read(65536):  # Buffer más grande (64KB)
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(folder, use_threading=True):
    """
    Encuentra duplicados de forma rápida.

    Optimizaciones:
    1. Compara primero por tamaño (muy rápido)
    2. Solo hashea archivos con tamaño duplicado
    3. Usa threading para procesar múltiples archivos en paralelo
    4. SHA256 es más rápido que MD5 en hardware moderno
    """

    # PASO 1: Agrupar archivos por tamaño (operación rápida)
    size_map = defaultdict(list)

    try:
        for dirpath, _, filenames in os.walk(folder):
            for f in filenames:
                full_path = os.path.join(dirpath, f)
                try:
                    file_size = os.path.getsize(full_path)
                    size_map[file_size].append(full_path)
                except (OSError, PermissionError):
                    pass
    except Exception as e:
        print(f"Error al escanear carpeta {folder}: {e}")

    # PASO 2: Solo procesar archivos que tienen duplicados potenciales (por tamaño)
    hashes = {}
    duplicates = []

    # Filtrar solo archivos con tamaño duplicado
    files_to_hash = [f for files in size_map.values() if len(files) > 1 for f in files]

    if not files_to_hash:
        return duplicates

    # PASO 3: Hashear archivos con threading (paralelo)
    if use_threading and len(files_to_hash) > 1:
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Mapear archivo a su hash
            future_to_file = {executor.submit(hash_file, f): f for f in files_to_hash}

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_hash = future.result()
                    if file_hash in hashes:
                        duplicates.append((file_path, hashes[file_hash]))
                    else:
                        hashes[file_hash] = file_path
                except Exception as e:
                    print(f"Error al hashear {file_path}: {e}")
    else:
        # Sin threading para archivos individuales
        for file_path in files_to_hash:
            try:
                file_hash = hash_file(file_path)
                if file_hash in hashes:
                    duplicates.append((file_path, hashes[file_hash]))
                else:
                    hashes[file_hash] = file_path
            except Exception as e:
                print(f"Error al hashear {file_path}: {e}")

    return duplicates


def delete_file(file_path):
    """Eliminar archivo con manejo de errores"""
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error al eliminar el archivo {file_path}: {e}")
        return False



