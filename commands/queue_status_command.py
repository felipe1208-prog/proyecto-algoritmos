from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class QueueStatusCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if args:
            try:
                target_id = int(args[0])
            except ValueError:
                print("Error: El identificador de ticket debe ser numérico.")
                return

            found = self.context.requests_history.find_by_predicate(
                lambda req: req.request_id == target_id
            )

            if found is None:
                print(f"Error: No se encontró el ticket #{target_id}.")
                return

            print(f"\n--- Detalle Ticket #{found.request_id} ({found.file_name}) ---")
            print(f"Estado: {found.status}")
            if found.status == "COMPLETED":
                print("\n[Respuesta de Gemini AI]:\n")
                print(found.response)
            elif found.status == "FAILED":
                print(f"\n[Fallo]: {found.error_message}")
            else:
                print("\nEl ticket se encuentra esperando en la cola o siendo procesado...")
            print("----------------------------------------------------\n")
            return

        if self.context.requests_history.is_empty():
            print("No se han emitido tickets de análisis en esta sesión.")
            return

        print("\n--- Estado de la Cola FIFO (IA Gemini) ---")
        for ticket in self.context.requests_history:
            print(f"  {ticket.summary()}")
        print("----------------------------------------")
        print("Para ver la respuesta detallada use: queue-status <id_ticket>\n")