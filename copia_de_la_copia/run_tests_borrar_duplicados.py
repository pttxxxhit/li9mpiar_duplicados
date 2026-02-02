import os
import tempfile
import time
from borrar_duplicados import find_duplicates, delete_file

print("Iniciando pruebas de borrar_duplicados...")

passed = 0
failed = 0

# Test 1: detectar duplicados simples
with tempfile.TemporaryDirectory() as tmpdir:
    f1 = os.path.join(tmpdir, 'file1.txt')
    f2 = os.path.join(tmpdir, 'file2.txt')
    f3 = os.path.join(tmpdir, 'file3.txt')

    with open(f1, 'w', encoding='utf-8') as fh:
        fh.write('contenido duplicado\n')
    with open(f2, 'w', encoding='utf-8') as fh:
        fh.write('contenido duplicado\n')
    with open(f3, 'w', encoding='utf-8') as fh:
        fh.write('contenido distinto\n')

    print(f"Carpeta temporal creada: {tmpdir}")

    dups = find_duplicates(tmpdir, use_threading=False)
    print('find_duplicates returned:', dups)

    # Esperamos al menos un duplicado que empareje f2 con f1 (o viceversa)
    pair_found = any((item[0] == f2 and item[1] == f1) or (item[0] == f1 and item[1] == f2) for item in dups)

    if pair_found:
        print('Test 1 PASSED: duplicado detectado correctamente')
        passed += 1
    else:
        print('Test 1 FAILED: duplicado no detectado')
        failed += 1

    # Test 2: eliminar duplicado detectado
    # Encontrar un duplicado para eliminar
    if dups:
        target = dups[0][0]
        print('Eliminando archivo:', target)
        ok = delete_file(target)
        time.sleep(0.1)
        exists_after = os.path.exists(target)
        if ok and not exists_after:
            print('Test 2 PASSED: delete_file eliminó el archivo correctamente')
            passed += 1
        else:
            print('Test 2 FAILED: delete_file no eliminó el archivo (ok=%s, exists_after=%s)' % (ok, exists_after))
            failed += 1
    else:
        print('Test 2 SKIPPED: no había duplicados para eliminar')

# Test 3: delete_file con ruta inexistente devuelve False
nonexistent = os.path.join(tempfile.gettempdir(), 'archivo_que_no_existe_12345.tmp')
ok = delete_file(nonexistent)
if not ok:
    print('Test 3 PASSED: delete_file devolvió False para archivo inexistente')
    passed += 1
else:
    print('Test 3 FAILED: delete_file devolvió True para archivo inexistente')
    failed += 1

print('\nResumen de pruebas:')
print('Passed:', passed)
print('Failed:', failed)

if failed == 0:
    print('TODAS LAS PRUEBAS PASARON ✅')
    exit(0)
else:
    print('HUBO FALLAS ❌')
    exit(2)
