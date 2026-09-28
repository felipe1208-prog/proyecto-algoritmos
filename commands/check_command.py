from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class CheckCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        active = self.context.active_file
        if active is None:
            print("Error: No hay ningún archivo activo para inspeccionar.")
            return

        diagnostics = self.context.static_analyzer.analyze(active.content)
        self.context.update_diagnostics(diagnostics)

        print(f"\n--- Diagnósticos del archivo '{active.name}' ---")
        if not diagnostics:
            print("✓ Sin anomalías ni errores de sintaxis detectados.")
        else:
            for d in diagnostics:
                print(f"  {d}")
            print(f"\nTotal: {len(diagnostics)} alerta(s). Puede ordenarlas usando: <criterio> sort <algoritmo>")
        print("--------------------------------------------------\n")