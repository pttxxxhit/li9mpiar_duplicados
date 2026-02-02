"""Runner sencillo para benchmarks de find_duplicates.
Uso: python run_bench.py <num_files> [dup_ratio] [file_size]
Ejemplo: python run_bench.py 800 0.2 1024
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.benchmark_duplicates import benchmark

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python run_bench.py <num_files> [dup_ratio] [file_size]')
        sys.exit(1)
    num_files = int(sys.argv[1])
    dup_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
    file_size = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    benchmark(num_files, dup_ratio, file_size)
