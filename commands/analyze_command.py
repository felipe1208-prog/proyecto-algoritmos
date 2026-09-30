from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class AnalyzeCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        active = self.context.active_file
        if active is None:
            print("Error: No hay ningún archivo activo para analizar.")
            return

        if not active.content.strip():
            print("Error: El archivo activo no contiene código para analizar.")
            return

        ticket = self.context.enqueue_analysis(active)
        print(f"Ticket #{ticket.request_id} encolado exitosamente en la cola FIFO.")
        print("El worker en segundo plano procesará la petición con la IA de Gemini.")
        print("Consulte el progreso con: queue-status")