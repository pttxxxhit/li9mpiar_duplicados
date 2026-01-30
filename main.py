import flet as ft
from flet import Colors as colors, Icons as icons
from borrar_duplicados import find_duplicates, delete_file
from app import organize_folder

import os
import threading
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        "selected_for_deletion": {},  # Dict {file_path: is_selected}
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

    # Botón "Eliminar seleccionados" (acción directa, sin confirmación)
    delete_all_btn = ft.ElevatedButton(
        "🗑️ ELIMINAR SELECCIONADOS",
        icon=icons.DELETE_SWEEP,
        bgcolor=colors.RED_900,
        color=colors.WHITE,
        visible=False,
        disabled=True,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # Botón "Seleccionar todos"
    select_all_btn = ft.TextButton(
        "Seleccionar todos",
        icon=icons.DONE_ALL,
        style=ft.ButtonStyle(
            color=colors.BLUE_400,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        visible=False,
    )

    # Botón "Deseleccionar todos"
    deselect_all_btn = ft.TextButton(
        "Deseleccionar todos",
        icon=icons.CLOSE,
        style=ft.ButtonStyle(
            color=colors.GREY_400,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        visible=False,
    )

    async def delete_selected_async(to_delete):
        # Deshabilitar botón y mostrar estado
        delete_all_btn.disabled = True
        delete_all_btn.bgcolor = colors.ORANGE_900
        delete_all_btn.text = "🔄 Eliminando..."
        delete_all_btn.update()

        # Ejecutar borrado en threads del event loop
        results = []
        for path in to_delete:
            results.append(asyncio.to_thread(delete_file, path))

        ok = fail = 0
        for res in await asyncio.gather(*results, return_exceptions=True):
            if isinstance(res, Exception) or res is False:
                fail += 1
            else:
                ok += 1

        # Refrescar UI
        scan_and_show_duplicates()

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

    def perform_delete_all(e=None):
        """Elimina los archivos seleccionados directamente"""
        to_delete = [file_path for file_path, is_selected in state["selected_for_deletion"].items() if is_selected]

        if not to_delete:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Selecciona al menos un archivo para eliminar", color=colors.WHITE),
                bgcolor=colors.BLUE_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Ejecutar eliminación async en el hilo principal de Flet
        page.run_task(delete_selected_async, to_delete)

    delete_all_btn.on_click = perform_delete_all

    def update_button_state():
        """Actualiza el estado del botón de eliminar según selecciones"""
        selected_count = sum(1 for is_sel in state["selected_for_deletion"].values() if is_sel)
        if selected_count > 0:
            delete_all_btn.disabled = False
            delete_all_btn.text = f"🗑️ ELIMINAR {selected_count} SELECCIONADOS"
            delete_all_btn.bgcolor = colors.RED_900
        else:
            delete_all_btn.disabled = True
            delete_all_btn.text = "🗑️ ELIMINAR SELECCIONADOS"
            delete_all_btn.bgcolor = colors.RED_900
        delete_all_btn.update()

    def toggle_selection(file_path, checkbox_ref):
        """Alterna la selección de un archivo"""
        state["selected_for_deletion"][file_path] = checkbox_ref.value
        update_button_state()

    def select_all_duplicates(_e=None):
        """Selecciona todos los duplicados"""
        for file_path in state["selected_for_deletion"]:
            state["selected_for_deletion"][file_path] = True
        # Actualizar checkboxes en la UI
        for control in duplicates_list.controls:
            if hasattr(control, 'content') and hasattr(control.content, 'controls'):
                for row in control.content.controls:
                    if isinstance(row, ft.Row) and len(row.controls) > 0:
                        if isinstance(row.controls[0], ft.Checkbox):
                            row.controls[0].value = True
        duplicates_list.update()
        update_button_state()

    def deselect_all_duplicates(_e=None):
        """Deselecciona todos los duplicados"""
        for file_path in state["selected_for_deletion"]:
            state["selected_for_deletion"][file_path] = False
        # Actualizar checkboxes en la UI
        for control in duplicates_list.controls:
            if hasattr(control, 'content') and hasattr(control.content, 'controls'):
                for row in control.content.controls:
                    if isinstance(row, ft.Row) and len(row.controls) > 0:
                        if isinstance(row.controls[0], ft.Checkbox):
                            row.controls[0].value = False
        duplicates_list.update()
        update_button_state()

    select_all_btn.on_click = select_all_duplicates
    deselect_all_btn.on_click = deselect_all_duplicates

    def scan_and_show_duplicates(e=None):
        folder = state["selected_folder"]
        if not folder or not os.path.isdir(folder):
            duplicates_counter.visible = False
            delete_all_btn.visible = False
            select_all_btn.visible = False
            deselect_all_btn.visible = False
            delete_all_btn.disabled = True
            duplicates_counter.update()
            delete_all_btn.update()
            return

        # Mostrar indicador de búsqueda
        duplicates_counter.content.controls[1].value = "🔍 Buscando duplicados..."
        duplicates_counter.content.controls[0].name = icons.HOURGLASS_EMPTY
        duplicates_counter.content.controls[0].color = colors.BLUE_400
        duplicates_counter.bgcolor = colors.with_opacity(0.15, colors.BLUE)
        duplicates_counter.visible = True
        duplicates_counter.update()

        duplicates = find_duplicates(folder)
        state["current_duplicates"] = duplicates
        state["selected_for_deletion"].clear()

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
            select_all_btn.visible = False
            deselect_all_btn.visible = False
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
            select_all_btn.visible = True
            deselect_all_btn.visible = True
            delete_all_btn.disabled = True

            # Crear items de la lista CON CHECKBOXES
            for idx, (dup, orig) in enumerate(duplicates, 1):
                state["selected_for_deletion"][dup] = False

                # Crear closure correcto para cada iteración
                def create_item(file_path, index, duplicate, original):
                    def on_checkbox_change(e):
                        state["selected_for_deletion"][file_path] = e.control.value
                        update_button_state()

                    def on_delete_click(_e):
                        delete_and_refresh(file_path)

                    checkbox = ft.Checkbox(
                        label="",
                        on_change=on_checkbox_change,
                        fill_color=colors.BLUE_400,
                    )

                    return ft.Container(
                        content=ft.Column([
                            ft.Row([
                                checkbox,
                                ft.Container(
                                    content=ft.Text(f"#{index}", size=12, weight=ft.FontWeight.BOLD),
                                    bgcolor=colors.BLUE_900,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=4,
                                ),
                                ft.Icon(icons.CONTENT_COPY, color=colors.BLUE_300, size=20),
                                ft.Text("Duplicado", color=colors.BLUE_300, weight=ft.FontWeight.BOLD),
                            ], spacing=8),
                            ft.Divider(height=1, color=colors.with_opacity(0.2, colors.WHITE)),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Duplicado:", size=11, color=colors.GREY_400),
                                    ft.Text(duplicate, size=12, color=colors.BLUE_200, selectable=True),
                                    ft.Text("Original:", size=11, color=colors.GREY_400),
                                    ft.Text(original, size=12, color=colors.GREEN_200, selectable=True),
                                ], expand=True, spacing=4),
                                ft.IconButton(
                                    icon=icons.DELETE_FOREVER,
                                    tooltip="Eliminar este duplicado",
                                    icon_color=colors.WHITE,
                                    bgcolor=colors.RED_700,
                                    icon_size=24,
                                    on_click=on_delete_click,
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ], spacing=8),
                        padding=16,
                        border_radius=8,
                        bgcolor=colors.with_opacity(0.08, colors.WHITE),
                        border=ft.border.all(1, colors.with_opacity(0.2, colors.BLUE)),
                    )

                duplicates_list.controls.append(create_item(dup, idx, dup, orig))

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
                "Encuentra y elimina archivos duplicados basándose en su contenido (hash SHA256)",
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
            ft.Row([
                select_all_btn,
                deselect_all_btn,
                delete_all_btn,
            ], spacing=10),
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

    # --- Fondo con imagen translúcida ---
    background_image = ft.Image(
        src="fondo.png",
        fit=ft.ImageFit.COVER,
        opacity=0.55,  # Translúcida (0.0 transparente, 1.0 opaco)
        expand=True,
    )

    main_content = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1, color=colors.with_opacity(0.3, colors.WHITE)),
            content_area,
        ],
        expand=True,
    )

    # Agregar margen inferior a la ventana
    root = ft.Column([
        ft.Stack(
            controls=[
                background_image,
                main_content,
            ],
            expand=True,
        ),
        ft.Container(height=20, bgcolor=colors.BLACK),  # Margen inferior
    ], expand=True)

    # --- Agrega el layout principal ---
    page.add(root)

if __name__ == "__main__":
    # Asegúrate de tener la carpeta "assets" con tu imagen "fondo.jpg"
    ft.app(target=main, assets_dir="assets")