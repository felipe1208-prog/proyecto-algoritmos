from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class DeleteCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if not args:
            print("Uso incorrecto: delete <nombre_archivo>")
            return

        file_name = args[0].strip()
        if self.context.delete_file(file_name):
            print(f"Archivo '{file_name}' eliminado de memoria.")
            if self.context.active_file:
                print(f"Nuevo archivo activo: '{self.context.active_file.name}'.")
            else:
                print("No quedan archivos abiertos en memoria.")
        else:
            print(f"Error: No se encontró el archivo '{file_name}' para eliminar.")