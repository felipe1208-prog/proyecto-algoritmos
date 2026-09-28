import shlex
from typing import Dict, List, Optional
from commands.command import Command


class CommandInvoker:

    def __init__(self) -> None:
        self._commands: Dict[str, Command] = {}

    def register(self, command_name: str, command: Command) -> None:
        self._commands[command_name.lower()] = command

    def execute_line(self, line: str) -> None:
        cleaned = line.strip()
        if not cleaned:
            return

        try:
            tokens: List[str] = shlex.split(cleaned)
        except ValueError:
            tokens = cleaned.split()

        if not tokens:
            return

        if len(tokens) >= 3 and tokens[1].lower() == "sort":
            criterion = tokens[0].lower()
            algorithm = tokens[2].lower()
            sort_command = self._commands.get("sort")
            if sort_command:
                sort_command.execute([criterion, algorithm])
            else:
                print("Error: El comando de ordenamiento no está disponible.")
            return

        primary_cmd = tokens[0].lower()
        args = tokens[1:]

        command = self._commands.get(primary_cmd)
        if command is not None:
            command.execute(args)
        else:
            print(f"Error: Comando '{primary_cmd}' no reconocido. Escriba 'help' o revise la sintaxis.")

    def get_registered_commands(self) -> List[str]:
        return sorted(list(self._commands.keys()))