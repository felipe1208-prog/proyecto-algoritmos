from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class ListCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if self.context.open_files.is_empty():
            print("No hay archivos abiertos en memoria.")
            return

        print("\n--- Archivos en Memoria ---")
        for idx, file_obj in enumerate(self.context.open_files):
            is_active = "*" if self.context.active_file and self.context.active_file.name == file_obj.name else " "
            print(f" {is_active} [{idx}] {file_obj.name} ({file_obj.line_count()} líneas)")
        print("---------------------------\n(* indica archivo activo)")