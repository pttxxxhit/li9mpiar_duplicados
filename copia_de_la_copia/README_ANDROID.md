# Migración Android — Instrucciones rápidas

Este documento guía la migración de la app Flet (`main_minimal.py`) a una app Android nativa (Kotlin + Jetpack Compose).

Resumen
- Estrategia recomendada: Jetpack Compose (nativa) para mejor rendimiento y experiencia móvil.

Prerequisitos
- Android Studio (Electric Eel o superior recomendado).
- JDK 11+.
- SDK Android con API 21–33 instalados.

Pasos iniciales
1. Abrir Android Studio → New Project → Empty Compose Activity. Package: `com.tuempresa.app`.
2. Copiar assets desde este repo:
   - `assets/fondo.png` → `app/src/main/res/drawable/fondo.png`.
   - Iconos → `app/src/main/res/mipmap-*/` o `res/drawable/` (usar vectores cuando sea posible).
   - Archivos de prueba `test_duplicados/` → `app/src/main/res/raw/` si es necesario.
3. Implementar estructura en Android Studio:
   - `MainActivity.kt` (Compose), `MainViewModel.kt`, `FileRepository.kt`.
4. Mapeo UI (rápido):
   - `ft.ListView` → `LazyColumn { items(list) { item -> Text(item.name) } }`
   - `ft.TextField` → `OutlinedTextField(value, { new -> ... })`
5. Manejo de archivos (recomendado): usar SAF + `DocumentFile` y `ContentResolver`.
6. Evitar `MANAGE_EXTERNAL_STORAGE` a menos que sea imprescindible. Usar permisos runtime para `READ_EXTERNAL_STORAGE` solo donde aplique.

Cómo probar eliminación
- Desde la app, seleccionar un archivo con el picker (SAF) y tocar "Eliminar". El repositorio debe llamar a `DocumentFile.delete()` o `ContentResolver.delete()` según corresponda, y luego refrescar la lista.

Notas
- Mantén `main_minimal.py` como referencia de comportamiento; migra la lógica no-UI por pasos y escribe tests unitarios para la lógica reimplementada.

Branch recomendado
- `android-migration`

Checklist corto
- [ ] Crear proyecto Compose en Android Studio
- [ ] Mover assets
- [ ] Implementar `FileRepository` con SAF
- [ ] Implementar `MainViewModel` + `MainScreen` (Compose)
- [ ] Probar permisos y eliminación en APIs 23, 29, 31, 33

Contacto
- Autor: (añade nombre)
