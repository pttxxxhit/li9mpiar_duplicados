import flet as ft
from flet import Colors as colors, Icons as icons
from borrar_duplicados import find_duplicates, delete_file
from app import organize_folder

import os

def main(page: ft.Page):
    # Configuración básica de la ventana
    page.title = "Automatización de Tareas"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK

    # Variables de estado
    state = {
        "current_duplicates": [],
        "current_view": "duplicates",
        "selected_folder": "",
        "organize_input_folder": "",
        "resize_input_folder": "",
        "resize_output_folder": "",
        "selecting_resize_output": False,
        "convert_input_file": "",
        "audio_input_folder": "",
        "audio_extraction_progress": 0,
        "total_videos": 0,
        "current_video": "",
        "pdf_input_folder": "",
        "rename_input_folder": "",
        "rename_option": "",
        "rename_value": ""
    }

    # --- Vista funcional para archivos duplicados ---
    selected_dir_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=14,
        color=colors.BLUE_200
    )
    # ListView con scroll para los duplicados
    duplicates_list = ft.ListView(
        expand=True,
        spacing=8,
        padding=0,
        auto_scroll=False,
    )

    # Contador de duplicados destacado
    duplicates_counter = ft.Container(
        content=ft.Row([
            ft.Icon(icons.INFO_OUTLINE, color=colors.BLUE_400, size=24),
            ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=colors.BLUE_400)
        ], tight=True, spacing=8),
        bgcolor=colors.with_opacity(0.15, colors.BLUE),
        padding=12,
        border_radius=8,
        border=ft.border.all(2, colors.BLUE_700),
        visible=False,
    )

    # Botón "Eliminar todos" con confirmación
    delete_all_btn = ft.ElevatedButton(
        "Eliminar todos los duplicados",
        icon=icons.DELETE_SWEEP,
        bgcolor=colors.RED_900,
        color=colors.WHITE,
        visible=False,
        disabled=True,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    def perform_delete_all(e=None):
        if not state["current_duplicates"]:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("No hay duplicados para eliminar", color=colors.WHITE),
                bgcolor=colors.BLUE_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Cerrar diálogo
        def close_dialog(_e):
            dialog.open = False
            page.update()

        # Función de confirmación
        def confirm_delete(_e):
            dialog.open = False
            page.update()

            delete_all_btn.disabled = True
            delete_all_btn.text = "Eliminando..."
            delete_all_btn.update()

            to_delete = [dup for dup, _ in state["current_duplicates"]]
            ok = fail = 0
            for dup in to_delete:
                try:
                    if delete_file(dup):
                        ok += 1
                    else:
                        fail += 1
                except Exception:
                    fail += 1

            # Refrescar
            scan_and_show_duplicates()

            # Mensaje de resultado
            if fail == 0:
                msg = f"✓ Eliminados {ok} duplicados correctamente"
                snack_color = colors.GREEN_700
            else:
                msg = f"⚠ Eliminados {ok}. Fallaron {fail}"
                snack_color = colors.ORANGE_700

            page.snack_bar = ft.SnackBar(
                content=ft.Text(msg, color=colors.WHITE, size=16),
                bgcolor=snack_color,
            )
            page.snack_bar.open = True
            page.update()

        # Diálogo de confirmación
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Confirmar eliminación", weight=ft.FontWeight.BOLD),
            content=ft.Text(
                f"¿Estás seguro de eliminar {len(state['current_duplicates'])} archivos duplicados?\n\n"
                "Esta acción no se puede deshacer.",
                size=14,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton(
                    "Eliminar todos",
                    on_click=confirm_delete,
                    style=ft.ButtonStyle(color=colors.RED_400),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    # Conectar el botón directamente a la acción (sin confirmación)
    delete_all_btn.on_click = perform_delete_all

    def scan_and_show_duplicates(e=None):
        folder = state["selected_folder"]
        if not folder or not os.path.isdir(folder):
            duplicates_counter.visible = False
            delete_all_btn.visible = False
            delete_all_btn.disabled = True
            duplicates_counter.update()
            delete_all_btn.update()
            return

        duplicates = find_duplicates(folder)
        state["current_duplicates"] = duplicates

        duplicates_list.controls.clear()

        if not duplicates:
            # No hay duplicados
            duplicates_counter.content.controls[1].value = "✓ No se encontraron archivos duplicados"
            duplicates_counter.content.controls[0].name = icons.CHECK_CIRCLE
            duplicates_counter.content.controls[0].color = colors.GREEN_400
            duplicates_counter.bgcolor = colors.with_opacity(0.15, colors.GREEN)
            duplicates_counter.border = ft.border.all(2, colors.GREEN_700)
            duplicates_counter.visible = True
            delete_all_btn.visible = False
            delete_all_btn.disabled = True
        else:
            # Hay duplicados
            duplicates_counter.content.controls[1].value = f"⚠ Se encontraron {len(duplicates)} archivos duplicados"
            duplicates_counter.content.controls[0].name = icons.WARNING
            duplicates_counter.content.controls[0].color = colors.ORANGE_400
            duplicates_counter.bgcolor = colors.with_opacity(0.15, colors.ORANGE)
            duplicates_counter.border = ft.border.all(2, colors.ORANGE_700)
            duplicates_counter.visible = True
            delete_all_btn.visible = True
            delete_all_btn.disabled = False
            delete_all_btn.text = f"Eliminar todos ({len(duplicates)})"

            # Crear items de la lista
            for idx, (dup, orig) in enumerate(duplicates, 1):
                def make_delete_fn(dup_file):
                    return lambda _ev: delete_and_refresh(dup_file)

                item = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(f"#{idx}", size=12, weight=ft.FontWeight.BOLD),
                                bgcolor=colors.BLUE_900,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=4,
                            ),
                            ft.Icon(icons.CONTENT_COPY, color=colors.BLUE_300, size=20),
                            ft.Text("Duplicado encontrado", color=colors.BLUE_300, weight=ft.FontWeight.BOLD),
                        ], spacing=8),
                        ft.Divider(height=1, color=colors.with_opacity(0.2, colors.WHITE)),
                        ft.Row([
                            ft.Column([
                                ft.Text("Duplicado:", size=11, color=colors.GREY_400),
                                ft.Text(dup, size=12, color=colors.BLUE_200, selectable=True),
                                ft.Text("Original:", size=11, color=colors.GREY_400),
                                ft.Text(orig, size=12, color=colors.GREEN_200, selectable=True),
                            ], expand=True, spacing=4),
                            ft.IconButton(
                                icon=icons.DELETE_FOREVER,
                                tooltip="Eliminar este duplicado",
                                icon_color=colors.WHITE,
                                bgcolor=colors.RED_700,
                                icon_size=24,
                                on_click=make_delete_fn(dup),
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ], spacing=8),
                    padding=16,
                    border_radius=8,
                    bgcolor=colors.with_opacity(0.08, colors.WHITE),
                    border=ft.border.all(1, colors.with_opacity(0.2, colors.BLUE)),
                )
                duplicates_list.controls.append(item)

        duplicates_list.update()
        duplicates_counter.update()
        delete_all_btn.update()

    def delete_and_refresh(dup_file):
        if delete_file(dup_file):
            state["current_duplicates"] = [item for item in state["current_duplicates"] if item[0] != dup_file]
            scan_and_show_duplicates()
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✓ Archivo eliminado: {os.path.basename(dup_file)}", color=colors.WHITE),
                bgcolor=colors.GREEN_700,
            )
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✗ Error al eliminar: {os.path.basename(dup_file)}", color=colors.WHITE),
                bgcolor=colors.RED_700,
            )
            page.snack_bar.open = True
            page.update()

    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            state["selected_folder"] = e.path
            selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
            selected_dir_text.update()
            scan_and_show_duplicates()

    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)

    duplicate_files_view = ft.Container(
        content=ft.Column([
            ft.Text("🗑️ Eliminar Archivos Duplicados", color=colors.BLUE_200, size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Encuentra y elimina archivos duplicados basándose en su contenido (hash MD5)",
                color=colors.GREY_400,
                size=13,
            ),
            ft.Divider(height=20),
            ft.Row([
                ft.ElevatedButton(
                    "📁 Seleccionar carpeta",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _ev: folder_picker.get_directory_path(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                ft.Container(
                    content=selected_dir_text,
                    expand=True,
                    padding=10,
                    bgcolor=colors.with_opacity(0.05, colors.WHITE),
                    border_radius=8,
                    border=ft.border.all(1, colors.with_opacity(0.2, colors.GREY)),
                ),
            ], spacing=10),
            ft.Container(height=10),
            duplicates_counter,
            ft.Container(height=10),
            delete_all_btn,
            ft.Divider(),
            ft.Container(
                content=duplicates_list,
                expand=True,
                border_radius=8,
            ),
        ], expand=True, spacing=0),
        expand=True,
        bgcolor=colors.with_opacity(0.25, colors.BLACK),
        padding=20,
        border_radius=12,
    )

    # --- Vista: Organizar archivos ---
    organize_selected_text = ft.Text("No se ha seleccionado ninguna carpeta", color=colors.BLUE_200)
    organize_result_text = ft.Text("", color=colors.BLUE_200)

    def handle_organize_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            state["organize_input_folder"] = e.path
            organize_selected_text.value = f"Carpeta a organizar: {e.path}"
            organize_selected_text.update()

    def run_organize(_ev=None):
        folder = state.get("organize_input_folder") or ""
        if not folder or not os.path.isdir(folder):
            organize_result_text.value = "Selecciona una carpeta válida para organizar."
            organize_result_text.color = colors.RED_400
            organize_result_text.update()
            return
        try:
            # Ejecutar organización
            organize_folder(folder)
            organize_result_text.value = "Organización completada."
            organize_result_text.color = colors.GREEN_400
        except Exception as ex:
            organize_result_text.value = f"Error al organizar: {ex}"
            organize_result_text.color = colors.RED_400
        organize_result_text.update()
        page.snack_bar = ft.SnackBar(ft.Text(organize_result_text.value), open=True)
        page.update()

    organize_picker = ft.FilePicker(on_result=handle_organize_folder_picker)
    page.overlay.append(organize_picker)

    organize_files_view = ft.Container(
        content=ft.Column(
            [
                ft.Text("Organizar archivos por tipo", color=colors.BLUE_200, size=24),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Seleccionar carpeta",
                            icon=icons.FOLDER_OPEN,
                            on_click=lambda _ev: organize_picker.get_directory_path(),
                        ),
                        organize_selected_text,
                        ft.ElevatedButton(
                            "Organizar",
                            icon=icons.CLEANING_SERVICES,
                            bgcolor=colors.BLUE_800,
                            color=colors.WHITE,
                            on_click=run_organize,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                ft.Divider(),
                organize_result_text,
                ft.Text(
                    "Moverá imágenes, videos, documentos, datasets y comprimidos a subcarpetas.",
                    color=colors.BLUE_200,
                    size=12,
                ),
            ],
            expand=True,
        ),
        expand=True,
        bgcolor=colors.with_opacity(0.25, colors.BLACK),
        padding=20,
        border_radius=8,
    )

    # --- Definición de vistas mínimas para evitar errores ---
    resize_files_view = ft.Container(
        content=ft.Text("Vista: Redimensionar imágenes", color=colors.BLUE_200), expand=True
    )
    convert_images_view = ft.Container(
        content=ft.Text("Vista: Convertir imágenes", color=colors.BLUE_200), expand=True
    )
    extract_audio_view = ft.Container(
        content=ft.Text("Vista: Extraer audio", color=colors.BLUE_200), expand=True
    )
    merge_pdfs_view = ft.Container(
        content=ft.Text("Vista: Fusionar PDFs", color=colors.BLUE_200), expand=True
    )
    rename_files_view = ft.Container(
        content=ft.Text("Vista: Renombrar archivos", color=colors.BLUE_200), expand=True
    )

    # El área de contenido principal inicia con la vista de duplicados
    content_area = ft.Container(content=duplicate_files_view, expand=True, padding=10)

    def change_view(e):
        selected = e.control.selected_index
        if selected == 0:
            state["current_view"] = "duplicates"
            content_area.content = duplicate_files_view
        elif selected == 1:
            state["current_view"] = "organize"
            content_area.content = organize_files_view
        elif selected == 2:
            state["current_view"] = "resize"
            content_area.content = resize_files_view
        elif selected == 3:
            state["current_view"] = "convert"
            content_area.content = convert_images_view
        elif selected == 4:
            state["current_view"] = "audio"
            content_area.content = extract_audio_view
        elif selected == 5:
            state["current_view"] = "merge_pdfs"
            content_area.content = merge_pdfs_view
        elif selected == 6:
            state["current_view"] = "rename"
            content_area.content = rename_files_view
        content_area.update()

    # Menú lateral
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=icons.DELETE_FOREVER,
                selected_icon=icons.DELETE_FOREVER,
                label="Duplicados",
            ),
            ft.NavigationRailDestination(
                icon=icons.FOLDER_COPY,
                selected_icon=icons.FOLDER_COPY,
                label="Organizar",
            ),
            ft.NavigationRailDestination(
                icon=icons.PHOTO_SIZE_SELECT_LARGE,
                selected_icon=icons.PHOTO_SIZE_SELECT_LARGE,
                label="Redimensionar",
            ),
            ft.NavigationRailDestination(
                icon=icons.TRANSFORM,
                selected_icon=icons.TRANSFORM,
                label="Convertir",
            ),
            ft.NavigationRailDestination(
                icon=icons.AUDIOTRACK,
                selected_icon=icons.AUDIOTRACK,
                label="Extraer Audio",
            ),
            ft.NavigationRailDestination(
                icon=icons.MERGE_TYPE,
                selected_icon=icons.MERGE_TYPE,
                label="Fusionar PDFs",
            ),
            ft.NavigationRailDestination(
                icon=icons.EDIT,
                selected_icon=icons.EDIT,
                label="Renombrar",
            ),
        ],
        on_change=change_view,
        bgcolor=colors.with_opacity(0.45, colors.GREY_900),
    )

    # --- Fondo con imagen repetida ---
    assets_img = os.path.join(os.getcwd(), "assets", "fondo.jpg")
    if os.path.exists(assets_img):
        background_image = ft.Image(
            src="fondo.jpg",
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.REPEAT,
            opacity=1.0,
            gapless_playback=True,
            expand=True,
        )
    else:
        background_image = None

    main_content = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1, color=colors.with_opacity(0.3, colors.WHITE)),
            content_area,
        ],
        expand=True,
    )

    if background_image is not None:
        root = ft.Stack(
            controls=[
                background_image,
                main_content,
            ],
            expand=True,
        )
        page.add(root)
    else:
        page.add(main_content)

if __name__ == "__main__":
    # Asegúrate de tener la carpeta "assets" con tu imagen "fondo.jpg"
    ft.app(target=main, assets_dir="assets")