"""Genera datasets sintéticos y mide el tiempo de find_duplicates.
Imprime comparativa con y sin threading.
"""
import sys
import os
# Asegurar que la carpeta raíz del proyecto esté en sys.path para importar tools
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import time
from tools.generate_synthetic import create_dataset
from borrar_duplicados import find_duplicates
import shutil


def benchmark(num_files=200, duplicate_ratio=0.2, file_size=1024):
    path = create_dataset(num_files=num_files, duplicate_ratio=duplicate_ratio, file_size=file_size)
    try:
        t0 = time.perf_counter()
        d1 = find_duplicates(path, use_threading=False)
        t1 = time.perf_counter()
        d2 = find_duplicates(path, use_threading=True)
        t2 = time.perf_counter()

        print(f"Dataset: files={num_files}, dup_ratio={duplicate_ratio}, size={file_size}B")
        print(f"No-threading: found={len(d1)} time={(t1-t0):.3f}s")
        print(f"Threading:    found={len(d2)} time={(t2-t1):.3f}s")
    finally:
        # borrar dataset para no consumir disco
        shutil.rmtree(path, ignore_errors=True)


if __name__ == '__main__':
    benchmark(200, 0.2, 1024)
