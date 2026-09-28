from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class UndoCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        active = self.context.active_file
        if active is None:
            print("Error: No hay ningún archivo activo.")
            return

        if active.undo():
            print(f"Deshecho realizado con éxito en '{active.name}'. (Estados restantes para deshacer: {active.undo_depth()})")
        else:
            print("No hay más acciones para deshacer en este archivo.")