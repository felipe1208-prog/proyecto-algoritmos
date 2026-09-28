from typing import List
from commands.command import Command


class HelpCommand(Command):

    def execute(self, args: List[str]) -> None:
        print("""
==================== COMANDOS DISPONIBLES ====================
Gestión de archivos en memoria:
  new <nombre>               : Crea un archivo y lo fija como activo.
  list                       : Lista los archivos abiertos (LinkedList).
  switch <nombre>            : Cambia el archivo activo.
  delete <nombre>            : Cierra y remueve un archivo de memoria.
  load <ruta_archivo>        : Carga un archivo físico al editor.

Edición y control de historial (Stack):
  show                       : Muestra el contenido del archivo activo.
  edit [texto]               : Anexa texto o abre el editor multilínea (:wq o END para salir).
  undo                       : Revierte la última acción (Undo Stack).
  redo                       : Reaplica la acción deshecha (Redo Stack).

Validación y Ordenamiento:
  check                      : Analiza sintaxis (delimitadores con Stack) y métricas.
  line sort mergesort        : Ordena alertas por número de línea con Mergesort.
  line sort shellsort        : Ordena alertas por número de línea con Shellsort.
  gravedad sort mergesort    : Ordena alertas por gravedad con Mergesort.
  gravedad sort shellsort    : Ordena alertas por gravedad con Shellsort.

Asistente IA (Groq & Queue FIFO):
  analyze                    : Encola el archivo activo para revisión con IA.
  queue-status               : Visualiza los tickets de la cola FIFO.
  queue-status <id>          : Muestra el diagnóstico generado por la IA para ese ticket.

Sistema:
  config                     : Muestra la configuración actual.
  config set <clave> <val>   : Modifica un parámetro de config.json.
  help                       : Muestra esta ayuda.
  exit                       : Detiene el worker y sale del IDE.
==============================================================
""")