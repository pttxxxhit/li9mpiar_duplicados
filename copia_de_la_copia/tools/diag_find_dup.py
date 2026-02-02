import time
from borrar_duplicados import find_duplicates

paths = ["test_duplicados"]

for p in paths:
    print(f"Scanning {p}...")
    t0 = time.time()
    try:
        dups = find_duplicates(p)
    except Exception as e:
        print("Error running find_duplicates:", e)
        dups = None
    t1 = time.time()
    print(f"Time: {t1-t0:.2f}s")
    if dups is None:
        continue
    print(f"Found {len(dups)} duplicate entries")
    for i, (dup, orig) in enumerate(dups[:10], 1):
        print(f"{i}: dup={dup}, orig={orig}")
    print('---')
