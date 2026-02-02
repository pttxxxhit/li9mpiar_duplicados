# Preparar y exportar a Android Studio (paso a paso y script)

Esto contiene la lista exacta de archivos que debes copiar y un script PowerShell opcional que automatiza la copia.

Archivos Kotlin (copiar a `app/src/main/java/<tu_package_path>/`):
- MainActivity.kt
- MainViewModel.kt
- FileRepository.kt
- MainScreen.kt

Snippets / soporte (copiar/pegar manualmente):
- gradle_module_snippet.gradle  → copiar dependencias a `app/build.gradle`
- AndroidManifest_snippet.xml  → insertar las líneas necesarias en `app/src/main/AndroidManifest.xml`

Assets:
- assets/fondo.png  → copiar a `app/src/main/res/drawable/fondo.png`

Script que copia todo automáticamente
- Archivo creado: `export_to_android.ps1` (en esta carpeta). Uso:
  - Ejemplo (PowerShell):
    ```powershell
    # copia los archivos al proyecto Android y reemplaza el package si indicas
    .\export_to_android.ps1 -DestinationProject "D:\AndroidProjects\MyApp" -PackageName "com.miempresa.miapp"
    ```

Qué hace el script `export_to_android.ps1`
- Crea la carpeta del package destino si no existe (ej: `app/src/main/java/com/miempresa/miapp/`).
- Copia los 4 archivos Kotlin al package destino y reemplaza la línea `package ...` por la que indiques.
- Copia `fondo.png` a `app/src/main/res/drawable/fondo.png`.
- Copia `gradle_module_snippet.gradle` y `AndroidManifest_snippet.xml` al directorio del proyecto destino (como archivos de ayuda) para que los pegues/combines manualmente.
- Muestra un resumen al terminar.

Pasos manuales mínimos después del script
1. Abrir Android Studio → Open Project (la carpeta del proyecto destino).
2. En `app/build.gradle` incorpora las dependencias del snippet `gradle_module_snippet.gradle` y sincroniza.
3. Abre `app/src/main/AndroidManifest.xml` y copia/mergea las entradas del archivo `AndroidManifest_snippet.xml` (si no quieres merge automático).
4. Compilar y ejecutar en un emulador/dispositivo.

Notas importantes
- Si tu package no es `com.example.app`, usa el parámetro `-PackageName` del script o edita manualmente la primera línea `package ...` de cada archivo Kotlin.
- El script no sobrescribe tu `AndroidManifest.xml` original: coloca `AndroidManifest_snippet.xml` para que lo revises e insertes en el lugar correcto (mejor revisar manualmente).
- Revisa versiones de Compose/Kotlin en `build.gradle` si el proyecto ya existía para evitar conflictos de versiones.

¿Quieres que genere también un ZIP con un proyecto Android Studio ya montado con estos archivos integrados (listo para abrir)? Responde "sí ZIP" y lo preparo.

---
Archivo único de referencia: este README y el script `export_to_android.ps1` (no se crearán más MD extra salvo que lo pidas).
