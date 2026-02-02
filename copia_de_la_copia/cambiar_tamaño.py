import os
from PIL import Image


def resize_single_image(input_file, output_folder, width, height):
    """
    Redimensiona una sola imagen y la guarda en la carpeta especificada.

    Args:
        input_file: Ruta completa del archivo de imagen
        output_folder: Carpeta donde guardar la imagen redimensionada
        width: Ancho en píxeles
        height: Alto en píxeles

    Returns:
        True si se redimensionó correctamente, False si hubo error
    """
    # Formatos soportados
    valid_extensions = (".jpeg", ".jpg", ".png", ".bmp", ".gif", ".tiff", ".webp")

    # Validar que sea un archivo de imagen
    if not input_file.lower().endswith(valid_extensions):
        raise ValueError(f"Formato no soportado. Use: {', '.join(valid_extensions)}")

    # Crear carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Obtener nombre del archivo
    filename = os.path.basename(input_file)
    name, ext = os.path.splitext(filename)
    output_file = os.path.join(output_folder, f"{name}_resized{ext}")

    try:
        with Image.open(input_file) as img:
            # Redimensionar
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            # Guardar con calidad óptima
            resized.save(output_file, quality=95, optimize=True)
        return True
    except Exception as exc:
        print(f"Error redimensionando {filename}: {exc}")
        return False


if __name__ == "__main__":
    # Ejemplo de uso
    resize_single_image("test_image.jpg", "output", 800, 600)
