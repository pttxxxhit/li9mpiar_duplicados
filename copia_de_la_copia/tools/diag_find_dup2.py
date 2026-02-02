import sys
import os
import time

# Asegurar que el root del proyecto esté en sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from borrar_duplicados import find_duplicates

TEST_FOLDERS = ['test_duplicados']

for folder in TEST_FOLDERS:
    path = os.path.join(ROOT, folder)
    print(f"Scanning: {path}")
    t0 = time.time()
    try:
        dups = find_duplicates(path)
    except Exception as e:
        print('Error running find_duplicates:', e)
        dups = None
    t1 = time.time()
    print(f"Time: {t1-t0:.2f}s")
    if dups is None:
        print('No result')
    else:
        print(f"Found {len(dups)} duplicate entries")
        for i, (dup, orig) in enumerate(dups[:10], 1):
            print(f"{i}: dup={dup}, orig={orig}")
    print('---')
