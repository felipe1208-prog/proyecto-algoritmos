from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class EditCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        active = self.context.active_file
        if active is None:
            print("Error: No hay ningún archivo activo. Use 'new <nombre>' primero.")
            return

        if args:
            new_line = " ".join(args)
            updated_content = (
                f"{active.content}\n{new_line}" if active.content else new_line
            )
            active.update_content(updated_content, record_history=True)
            print(f"Línea añadida. Total de líneas: {active.line_count()}.")
        else:
            print("Modo edición multilínea activo. Escriba ':wq' o 'END' en una línea vacía para guardar:")
            lines_buffer: List[str] = []
            while True:
                try:
                    entry = input("> ")
                except (EOFError, KeyboardInterrupt):
                    break
                if entry.strip() in (":wq", "END"):
                    break
                lines_buffer.append(entry)

            new_text = "\n".join(lines_buffer)
            active.update_content(new_text, record_history=True)
            print(f"Contenido actualizado ({active.line_count()} líneas). Historial registrado en la pila.")