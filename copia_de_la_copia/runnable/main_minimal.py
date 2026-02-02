"""
Versión mínima estable de runnable/main_minimal.py
- UI simple: seleccionar carpeta, buscar duplicados, lista con checkboxes y eliminar seleccionados.
- FilePicker creado de forma compatible (asignando on_result/on_change como atributo).
- Evita llamadas a APIs que dependan de versiones concretas de flet (no usa parametros incompatibles).
"""

import flet as ft
from flet import Colors as colors, Icons as icons
from borrar_duplicados import find_duplicates, delete_file

import os
import threading
from concurrent.futures import ThreadPoolExecutor

APP_TITLE = "Duplicados - Minimal (estable)"
WINDOW_SIZE = (900, 640)


def main(page: ft.Page):
    page.title = APP_TITLE
    page.window.width, page.window.height = WINDOW_SIZE
    page.padding = 12
    page.bgcolor = colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK

    state = {"folder": "", "duplicates": [], "checkboxes": {}}

    selected_dir = ft.Text("No se ha seleccionado ninguna carpeta", color=colors.BLUE_200)
    status_text = ft.Text("", color=colors.GREY_400)
    duplicates_list = ft.ListView(expand=True, spacing=8)

    # FilePicker compatible
    def on_folder_result(e):
        path = getattr(e, 'path', None) or getattr(e, 'selected_path', None)
        if path:
            state['folder'] = path
            selected_dir.value = f"Carpeta: {path}"
            selected_dir.update()
            scan()

    # Crear FilePicker sin argumentos y asignar handler por atributo (más compatible)
    folder_picker = ft.FilePicker()
    try:
        folder_picker.on_result = on_folder_result
    except Exception:
        try:
            folder_picker.on_change = on_folder_result
        except Exception:
            pass
    page.overlay.append(folder_picker)

    # Actions
    def scan():
        folder = state.get('folder')
        if not folder or not os.path.isdir(folder):
            status_text.value = 'Selecciona una carpeta válida'
            status_text.update()
            return

        status_text.value = 'Buscando...'
        status_text.update()

        def worker():
            duplicates = find_duplicates(folder) or []
            state['duplicates'] = duplicates

            def update_ui():
                duplicates_list.controls.clear()
                state['checkboxes'].clear()
                for idx, (dup, orig) in enumerate(duplicates, start=1):
                    cb = ft.Checkbox(label=f"{os.path.basename(dup)}", value=False)
                    state['checkboxes'][dup] = cb
                    row = ft.Row([cb, ft.Text(orig, selectable=True), ft.IconButton(icons.DELETE, on_click=lambda e, p=dup: single_delete(p))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    duplicates_list.controls.append(ft.Container(content=row, padding=6))
                status_text.value = f"{len(duplicates)} duplicados encontrados"
                status_text.update()
                duplicates_list.update()

            page.call_from_thread(update_ui)

        threading.Thread(target=worker, daemon=True).start()

    def single_delete(path):
        ok = delete_file(path)
        if ok:
            scan()
            page.snack_bar = ft.SnackBar(ft.Text('Archivo eliminado', color=colors.WHITE), bgcolor=colors.GREEN_700)
            page.snack_bar.open = True
            page.update()

    def delete_selected(e=None):
        to_delete = [p for p, cb in state['checkboxes'].items() if getattr(cb, 'value', False)]
        if not to_delete:
            page.snack_bar = ft.SnackBar(ft.Text('No hay archivos seleccionados', color=colors.WHITE), bgcolor=colors.ORANGE_400)
            page.snack_bar.open = True
            page.update()
            return

        def worker():
            ok = fail = 0
            for p in to_delete:
                try:
                    if delete_file(p):
                        ok += 1
                    else:
                        fail += 1
                except Exception:
                    fail += 1

            def finish():
                scan()
                page.snack_bar = ft.SnackBar(ft.Text(f"✓ Eliminados: {ok}. Fallidos: {fail}", color=colors.WHITE), bgcolor=colors.GREEN_700 if fail==0 else colors.ORANGE_400)
                page.snack_bar.open = True
                page.update()

            page.call_from_thread(finish)

        threading.Thread(target=worker, daemon=True).start()

    # Buttons
    btn_select_folder = ft.ElevatedButton('📁 Seleccionar carpeta', on_click=lambda e: folder_picker.get_directory_path())
    btn_scan = ft.ElevatedButton('🔍 Buscar duplicados', on_click=lambda e: scan())
    btn_select_all = ft.ElevatedButton('Seleccionar todos', on_click=lambda e: [setattr(cb, "value", True) for cb in state['checkboxes'].values()] or duplicates_list.update())
    btn_deselect_all = ft.ElevatedButton('Deseleccionar', on_click=lambda e: [setattr(cb, "value", False) for cb in state['checkboxes'].values()] or duplicates_list.update())
    btn_delete_selected = ft.ElevatedButton('🗑️ ELIMINAR', on_click=delete_selected, bgcolor=colors.RED_700)

    left = ft.Column([btn_select_folder, btn_scan, btn_select_all], spacing=8, width=300)
    right = ft.Column([btn_deselect_all, btn_delete_selected], spacing=8, width=140)

    content = ft.Row([left, right, ft.VerticalDivider(), ft.Column([selected_dir, ft.Container(height=8), status_text, ft.Container(height=8), duplicates_list], expand=True)], expand=True)

    page.add(content)
    page.update()


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
