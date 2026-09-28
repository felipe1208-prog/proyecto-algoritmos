from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class SwitchCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if not args:
            print("Uso incorrecto: switch <nombre_archivo>")
            return

        target_name = args[0].strip()
        if self.context.switch_file(target_name):
            print(f"Archivo activo cambiado a: '{target_name}'.")
        else:
            print(f"Error: El archivo '{target_name}' no existe en memoria.")