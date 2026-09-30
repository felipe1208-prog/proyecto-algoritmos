from typing import List
from commands.command import Command
from core.editor_context import EditorContext


class ConfigCommand(Command):

    def __init__(self, context: EditorContext) -> None:
        self.context: EditorContext = context

    def execute(self, args: List[str]) -> None:
        if not args:
            print("\n--- Configuración Actual ---")
            for key, val in self.context.config_service.get_all().items():
                masked_val = "***" if "key" in key.lower() and val else val
                print(f"  {key}: {masked_val}")
            print("----------------------------\n")
            return

        if len(args) >= 3 and args[0].lower() == "set":
            key = args[1]
            val = " ".join(args[2:]).strip("\"'")
            if self.context.config_service.set(key, val):
                # Sincronización en caliente con el servicio de Gemini
                if key == "gemini_model":
                    self.context.ai_service.model = val
                elif key == "gemini_api_key":
                    self.context.ai_service.api_key = val
                elif key == "timeout_seconds":
                    self.context.ai_service.timeout = int(val)

                print(f"Parámetro '{key}' actualizado a '{val}'.")
            else:
                print(f"Error al persistir la clave '{key}'.")
        else:
            print("Uso: config | config set <clave> <valor>")