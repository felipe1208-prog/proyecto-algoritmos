from typing import List
from commands.command import Command
from core.editor_context import EditorContext
from algorithms.merge_sort import MergeSort
from algorithms.shell_sort import ShellSort


class SortCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if len(args) < 2:
            print("Uso incorrecto: <criterio> sort <algoritmo>")
            print("Criterios admitidos: line | gravedad")
            print("Algoritmos admitidos: mergesort | shellsort")
            return

        criterion = args[0].lower()
        algorithm = args[1].lower()

        if criterion not in ("line", "gravedad", "severity"):
            print(f"Error: Criterio desconocido '{criterion}'. Use 'line' o 'gravedad'.")
            return

        if algorithm not in ("mergesort", "shellsort"):
            print(f"Error: Algoritmo desconocido '{algorithm}'. Use 'mergesort' o 'shellsort'.")
            return

        diagnostics = self.context.last_diagnostics
        if not diagnostics:
            print("No hay diagnósticos cargados. Ejecute 'check' sobre el archivo activo primero.")
            return

        if algorithm == "mergesort":
            sorted_list = MergeSort.sort(diagnostics, criterion=criterion)
        else:
            sorted_list = ShellSort.sort(diagnostics, criterion=criterion)

        print(f"\n--- Alertas ordenadas por [{criterion.upper()}] usando [{algorithm.upper()}] ---")
        for diag in sorted_list:
            print(f"  {diag}")
        print("------------------------------------------------------------------------\n")