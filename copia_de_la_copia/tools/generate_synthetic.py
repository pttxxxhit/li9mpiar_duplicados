"""Crea un conjunto de archivos sintéticos para probar find_duplicates.
Uso:
    from generate_synthetic import create_dataset
    path = create_dataset(num_files=200, duplicate_ratio=0.2, file_size=1024)

Devuelve la ruta del directorio creado.
"""
import os
import tempfile
import random
import shutil


def create_dataset(num_files=100, duplicate_ratio=0.1, file_size=1024, seed=None):
    """Crear un directorio temporal con `num_files` archivos.
    duplicate_ratio: fracción de archivos que serán copias de otros (0..1)
    file_size: bytes por archivo (para archivos no duplicados se generan contenidos aleatorios)
    """
    if seed is not None:
        random.seed(seed)

    tmpdir = tempfile.mkdtemp(prefix="dup_test_")

    # Número de duplicados (archivos que serán copias de un original)
    num_duplicates = int(num_files * duplicate_ratio)
    num_unique = num_files - num_duplicates

    unique_files = []

    # Crear archivos únicos
    for i in range(num_unique):
        path = os.path.join(tmpdir, f"unique_{i}.bin")
        with open(path, "wb") as fh:
            fh.write(os.urandom(file_size))
        unique_files.append(path)

    # Crear duplicados copiando contenidos de archivos aleatorios entre los únicos
    for j in range(num_duplicates):
        src = random.choice(unique_files)
        dest = os.path.join(tmpdir, f"dup_{j}.bin")
        shutil.copyfile(src, dest)

    return tmpdir


if __name__ == "__main__":
    print(create_dataset(50, 0.2, 1024))
