from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class ShowCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        active = self.context.active_file
        if active is None:
            print("Error: No hay ningún archivo activo para mostrar.")
            return

        lines = active.get_lines()
        print(f"\n--- Contenido de '{active.name}' ({len(lines)} líneas) ---")
        if not lines:
            print("  (Archivo vacío)")
        else:
            for idx, line in enumerate(lines, start=1):
                print(f"{idx:4d} | {line}")
        print("--------------------------------------------------\n")