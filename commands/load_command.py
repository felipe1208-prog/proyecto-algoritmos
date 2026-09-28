import os
from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class LoadCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if not args:
            print("Uso incorrecto: load <ruta_archivo>")
            return

        filepath = args[0].strip()
        if not os.path.exists(filepath):
            print(f"Error: La ruta '{filepath}' no existe.")
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            filename = os.path.basename(filepath)
            existing = self.context.find_file(filename)

            if existing is not None:
                existing.update_content(content, record_history=True)
                self.context.active_file = existing
                print(f"Archivo '{filename}' recargado y establecido como activo.")
            else:
                self.context.create_file(filename, content)
                print(f"Archivo '{filename}' cargado exitosamente en memoria ({len(content.splitlines())} líneas).")

        except Exception as e:
            print(f"Error al leer el archivo: {e}")