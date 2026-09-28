from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class NewCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if not args:
            print("Uso incorrecto: new <nombre_archivo>")
            return

        file_name = args[0].strip()
        created = self.context.create_file(file_name)

        if created is not None:
            print(f"Archivo '{file_name}' creado con éxito y establecido como activo.")
        else:
            print(f"Error: Ya existe un archivo abierto con el nombre '{file_name}'.")