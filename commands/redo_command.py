from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class RedoCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        active = self.context.active_file
        if active is None:
            print("Error: No hay ningún archivo activo.")
            return

        if active.redo():
            print(f"Rehecho realizado con éxito en '{active.name}'. (Estados restantes para rehacer: {active.redo_depth()})")
        else:
            print("No hay más acciones para rehacer en este archivo.")