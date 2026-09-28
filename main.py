import sys
from core.editor_context import EditorContext
from core.command_invoker import CommandInvoker

from commands.new_command import NewCommand
from commands.list_command import ListCommand
from commands.switch_command import SwitchCommand
from commands.delete_command import DeleteCommand
from commands.config_command import ConfigCommand
from commands.show_command import ShowCommand
from commands.edit_command import EditCommand
from commands.load_command import LoadCommand
from commands.undo_command import UndoCommand
from commands.redo_command import RedoCommand
from commands.check_command import CheckCommand
from commands.sort_command import SortCommand
from commands.analyze_command import AnalyzeCommand
from commands.queue_status_command import QueueStatusCommand
from commands.help_command import HelpCommand


def setup_invoker(context: EditorContext) -> CommandInvoker:
    invoker = CommandInvoker()

    invoker.register("new", NewCommand(context))
    invoker.register("list", ListCommand(context))
    invoker.register("switch", SwitchCommand(context))
    invoker.register("delete", DeleteCommand(context))
    invoker.register("load", LoadCommand(context))

    invoker.register("show", ShowCommand(context))
    invoker.register("view", ShowCommand(context))
    invoker.register("edit", EditCommand(context))
    invoker.register("undo", UndoCommand(context))
    invoker.register("redo", RedoCommand(context))

    invoker.register("check", CheckCommand(context))
    invoker.register("sort", SortCommand(context))

    invoker.register("analyze", AnalyzeCommand(context))
    invoker.register("queue-status", QueueStatusCommand(context))

    invoker.register("config", ConfigCommand(context))
    invoker.register("help", HelpCommand())

    return invoker


def main() -> None:
    """Bucle principal de la interfaz de consola del IDE."""
    context = EditorContext(config_path="config.json", env_path=".env")
    invoker = setup_invoker(context)

    print("=" * 60)
    print("      SYNTHETIX STUDIO CLI - IDE DE CHATBOTS & CODIGO     ")
    print("  Algoritmos y Estructuras 2 - Universidad Jose Antonio Paez")
    print("=" * 60)
    print("Escriba 'help' para ver los comandos o 'exit' para salir.\n")

    try:
        while True:
            active_info = context.active_file.name if context.active_file else "ninguno"
            prompt = f"SynthetixStudio [{active_info}] > "

            try:
                user_input = input(prompt)
            except EOFError:
                break

            cleaned_input = user_input.strip()
            if not cleaned_input:
                continue

            if cleaned_input.lower() in ("exit", "quit"):
                print("\nCerrando servicios y finalizando Synthetix Studio...")
                break

            invoker.execute_line(cleaned_input)

    except KeyboardInterrupt:
        print("\n\nInterrupción manual detectada.")
    finally:
        context.shutdown()
        print("Sesión finalizada.")
        sys.exit(0)


if __name__ == "__main__":
    main()