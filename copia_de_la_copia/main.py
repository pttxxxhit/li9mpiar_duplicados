import flet as ft
from flet import Colors as colors, Icons as icons
from borrar_duplicados import find_duplicates, delete_file

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def main(page: ft.Page):
    # Configuración básica de la ventana
    page.title = "Automatización de Tareas"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK

    # Variables de estado (solo lo necesario para duplicados)
    state = {
        "current_duplicates": [],
        "selected_for_deletion": {},  # Dict {file_path: is_selected}
        "current_view": "duplicates",
        "selected_folder": "",
    }

    # Referencias a los checkboxes para actualizar la UI sin hacer introspección
    state["checkbox_refs"] = {}

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

    # Crear referencias explícitas para el icono y el texto del contador
    duplicates_icon = ft.Icon(icons.INFO_OUTLINE, color=colors.BLUE_400, size=24)
    duplicates_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=colors.BLUE_400)
    duplicates_counter = ft.Container(
        content=ft.Row([duplicates_icon, duplicates_text], tight=True, spacing=8),
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

    def perform_delete_all(e=None):
        """Elimina los archivos seleccionados directamente"""
        # Obtener solo los archivos seleccionados
        to_delete = [file_path for file_path, is_selected in state["selected_for_deletion"].items() if is_selected]

        if not to_delete:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Selecciona al menos un archivo para eliminar", color=colors.WHITE),
                bgcolor=colors.BLUE_700,
            )
            page.snack_bar.open = True
            page.update()
            return

        # Cambiar botón inmediatamente
        delete_all_btn.disabled = True
        delete_all_btn.bgcolor = colors.ORANGE_900
        delete_all_btn.text = "🔄 Eliminando..."
        delete_all_btn.update()

        # Función que elimina y actualiza
        def delete_and_update():
            ok = fail = 0
            max_workers = min(8, len(to_delete))

            # Eliminar archivos en paralelo o secuencial
            if len(to_delete) > 1:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {executor.submit(delete_file, dup): dup for dup in to_delete}
                    for future in as_completed(futures):
                        try:
                            if future.result():
                                ok += 1
                            else:
                                fail += 1
                        except Exception:
                            fail += 1
            else:
                for dup in to_delete:
                    try:
                        if delete_file(dup):
                            ok += 1
                        else:
                            fail += 1
                    except Exception:
                        fail += 1

            time.sleep(0.5)

            # Actualizar UI
            try:
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
            except Exception:
                pass

        # Iniciar thread de eliminación
        thread = threading.Thread(target=delete_and_update, daemon=True)
        thread.start()


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
        for file_path, cb in state.get("checkbox_refs", {}).items():
            try:
                cb.value = True
                state["selected_for_deletion"][file_path] = True
            except Exception:
                state["selected_for_deletion"][file_path] = True
        duplicates_list.update()
        update_button_state()

    def deselect_all_duplicates(_e=None):
        """Deselecciona todos los duplicados"""
        for file_path, cb in state.get("checkbox_refs", {}).items():
            try:
                cb.value = False
                state["selected_for_deletion"][file_path] = False
            except Exception:
                state["selected_for_deletion"][file_path] = False
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
        duplicates_text.value = "🔍 Buscando duplicados..."
        duplicates_icon.name = icons.HOURGLASS_EMPTY
        duplicates_icon.color = colors.BLUE_400
        duplicates_counter.bgcolor = colors.with_opacity(0.15, colors.BLUE)
        duplicates_counter.visible = True
        duplicates_text.update()
        duplicates_icon.update()
        duplicates_counter.update()

        duplicates = find_duplicates(folder)
        state["current_duplicates"] = duplicates
        # Limpiar referencias previas a checkboxes
        state["checkbox_refs"].clear()
        state["selected_for_deletion"].clear()

        duplicates_list.controls.clear()

        if not duplicates:
            # No hay duplicados
            duplicates_text.value = "✓ No se encontraron archivos duplicados"
            duplicates_icon.name = icons.CHECK_CIRCLE
            duplicates_icon.color = colors.GREEN_400
            duplicates_counter.bgcolor = colors.with_opacity(0.15, colors.GREEN)
            duplicates_counter.border = ft.border.all(2, colors.GREEN_700)
            duplicates_counter.visible = True
            delete_all_btn.visible = False
            select_all_btn.visible = False
            deselect_all_btn.visible = False
            delete_all_btn.disabled = True
        else:
            # Hay duplicados
            duplicates_text.value = f"⚠ Se encontraron {len(duplicates)} archivos duplicados"
            duplicates_icon.name = icons.WARNING
            duplicates_icon.color = colors.ORANGE_400
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
+
+                    # Guardar referencia para actualizaciones globales (select all / deselect all)
+                    state["checkbox_refs"][file_path] = checkbox

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
        duplicates_icon.update()
        duplicates_text.update()
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

    # El área de contenido principal inicia con la vista de duplicados
    content_area = ft.Container(content=duplicate_files_view, expand=True, padding=10)

    def change_view(e):
        # Solo existe la vista de duplicados ahora
        state["current_view"] = "duplicates"
        content_area.content = duplicate_files_view
        content_area.update()

    # Menú lateral reducido: solo 'Duplicados'
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