# ASSETS_MANIFEST

Inventario de assets para migración Android

Origen -> Destino sugerido

- assets/fondo.png -> app/src/main/res/drawable/fondo.png
- assets/ (otros) -> app/src/main/res/drawable/
- images_resized/ -> app/src/main/res/drawable/ (optimizar tamaños y generar mdpi/hdpi/xhdpi)
- test_duplicados/*.csv -> app/src/main/res/raw/ (si necesario como datos de ejemplo)

Notas:
- Para iconos de la app, generar `ic_launcher` en carpeta `mipmap-*/` con las resoluciones necesarias.
- Preferir vectores (`.svg` → `VectorDrawable`) para iconos simples.
