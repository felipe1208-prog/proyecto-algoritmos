# Synthetix Studio

Mini IDE de consola desarrollado en Python para gestionar archivos de código en memoria, editarlos con historial, ejecutar un análisis estático y solicitar recomendaciones a Gemini. La aplicación organiza las acciones con el patrón Command y utiliza implementaciones propias de listas enlazadas, pilas y cola.

Proyecto académico de Algoritmos y Estructuras II, Universidad José Antonio Páez.

## Funcionalidades

- Crear, listar, seleccionar, eliminar y cargar archivos en la sesión.
- Mostrar y editar el contenido del archivo activo.
- Deshacer y rehacer cambios con pilas independientes por archivo.
- Revisar balanceo de `()`, `{}` y `[]`, además de reglas estáticas sencillas.
- Ordenar los diagnósticos por línea o gravedad con Mergesort o Shellsort.
- Encolar solicitudes de análisis de Gemini en una cola FIFO y consultar su estado mediante tickets.
- Leer y modificar parámetros de `config.json`.

## Requisitos

- Python 3 instalado.
- Una clave de API de Gemini para utilizar el análisis con IA.
- Conexión a Internet para enviar solicitudes a Gemini.

El proyecto utiliza módulos de la biblioteca estándar de Python; no necesita instalar paquetes de terceros.

## Instalación y ejecución

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone https://github.com/felipe1208-prog/proyecto-algoritmos.git
cd proyecto-algoritmos
```

Crea un entorno virtual (opcional, recomendado):

```bash
python -m venv .venv
```

Actívalo en Windows:

```powershell
.venv\Scripts\Activate.ps1
```

O en macOS/Linux:

```bash
source .venv/bin/activate
```

Configura la clave de Gemini como se indica abajo y ejecuta:

```bash
python main.py
```

La aplicación inicia la consola interactiva. Escribe `help` para ver los comandos disponibles y `exit` para cerrar la sesión.

## Configuración

La aplicación carga `config.json` al iniciar. Si no existe, crea uno con valores predeterminados. Ejemplo:

```json
{
  "gemini_api_key": "",
  "gemini_model": "gemini-2.5-flash",
  "timeout_seconds": 30,
  "backup_directory": "./backups",
  "max_line_length": 80
}
```

Para usar Gemini, coloca tu clave en el archivo local `.env`:

```dotenv
apiAI=TU_CLAVE_DE_GEMINI
```

El repositorio incluye `.env.example` como referencia. No publiques ni compartas tu clave; `.env` está excluido de Git. También se puede establecer `gemini_api_key` en `config.json`, pero se recomienda mantener credenciales fuera del archivo versionado.

La integración utiliza el endpoint `generateContent` de Google Gemini y el modelo configurado en `gemini_model`. La URL base no se configura por separado. `timeout_seconds` controla el tiempo máximo de espera de la solicitud y `max_line_length` el umbral para alertas de líneas extensas.

## Comandos de la CLI

| Comando | Descripción |
| --- | --- |
| `new <nombre>` | Crea un archivo vacío en memoria y lo activa. |
| `list` | Lista los archivos y marca el activo con `*`. |
| `switch <nombre>` | Cambia el archivo activo. |
| `delete <nombre>` | Elimina un archivo de la sesión. |
| `load <ruta>` | Lee un archivo local y lo carga en memoria. |
| `show` o `view` | Muestra el contenido del archivo activo con números de línea. |
| `edit <texto>` | Añade una línea al final del contenido. |
| `edit` | Abre la edición multilínea; escribe `:wq` o `END` en una línea para terminar. |
| `undo` | Deshace el último cambio del archivo activo. |
| `redo` | Rehace el cambio deshecho. |
| `check` | Genera y muestra diagnósticos del archivo activo. |
| `<criterio> sort <algoritmo>` | Ordena los diagnósticos existentes. |
| `analyze` | Encola el código activo para su análisis con Gemini. |
| `queue-status` | Muestra los tickets emitidos en la sesión. |
| `queue-status <id>` | Muestra el estado o resultado del ticket indicado. |
| `config` | Muestra los parámetros actuales, ocultando la clave si está configurada. |
| `config set <clave> <valor>` | Cambia y guarda un parámetro en `config.json`. |
| `help` | Muestra la ayuda de la consola. |
| `exit` o `quit` | Cierra la aplicación. |

### Ejemplo de sesión

```text
new ejemplo.py
edit def sumar(a, b):
edit     return a + b
show
check
analyze
queue-status
queue-status 1
```

Los criterios de ordenamiento son `line` y `gravedad` (también se acepta `severity`). Los algoritmos son `mergesort` y `shellsort`. Por ejemplo:

```text
gravedad sort shellsort
```

Ejecuta `check` antes de `sort`: el ordenamiento usa los diagnósticos producidos por la última revisión del código activo.

## Arquitectura

```text
main.py                   Inicio de la CLI y registro de comandos
commands/                 Acciones del usuario implementadas como comandos
core/
  command_invoker.py      Interpreta y despacha las instrucciones
  editor_context.py       Mantiene archivos, diagnósticos y servicios de sesión
models/                   Archivos, diagnósticos y solicitudes de análisis
structures/               Nodo, lista enlazada, pila y cola propias
algorithms/               Implementaciones de Mergesort y Shellsort
services/                 Configuración, análisis estático, Gemini y worker FIFO
config.json               Configuración de ejemplo
.env.example              Plantilla local para la clave de Gemini
```

`CommandInvoker` interpreta cada línea y ejecuta el objeto de comando asociado. `EditorContext` coordina los archivos en memoria y los servicios. Cada `CodeFile` conserva su propio historial Undo/Redo. Un worker en segundo plano extrae las solicitudes de una cola FIFO y las procesa de forma secuencial.

## Estructuras y complejidad

| Componente | Operaciones principales | Complejidad |
| --- | --- | --- |
| Lista enlazada simple | Búsqueda, eliminación y recorrido de archivos | O(n) |
| Pila enlazada | `push`, `pop` y `peek` | O(1) |
| Cola enlazada | `enqueue`, `dequeue` y `peek` | O(1) |
| Verificador de delimitadores | Recorre el código y usa una pila auxiliar | O(c) tiempo y O(d) espacio, con `c` caracteres y `d` delimitadores abiertos |
| Análisis estático | Revisa el código por caracteres y líneas | O(c) tiempo |
| Mergesort | Ordenamiento de diagnósticos | O(n log n) tiempo y O(n) espacio adicional |
| Shellsort | Saltos decrecientes por mitades | O(n²) en el peor caso para esta secuencia de saltos; O(1) espacio adicional |

Las estructuras lineales están implementadas en `structures/`; los algoritmos de ordenamiento no usan `list.sort()` ni `sorted()`.

## Alcance del análisis

`check` valida el anidamiento de delimitadores y detecta reglas simples de estilo: líneas que superan el máximo configurado, espacios al final, bloques de tres o más líneas vacías e indentación de al menos 16 espacios. No sustituye al compilador ni a un analizador sintáctico específico de cada lenguaje.

`analyze` envía el contenido a Gemini para recibir una respuesta en texto con observaciones y recomendaciones. El formato y el contenido de la respuesta dependen del modelo; no se extraen ni validan automáticamente métricas estructuradas de complejidad Big O.

## Notas de implementación

- `backup_directory` está disponible como parámetro de configuración, pero la creación automática de respaldos todavía no está implementada.
- El enunciado también solicita rutas y archivos de logs de errores; actualmente no hay un sistema de logs configurado.
- La cola permite procesar solicitudes de IA de forma secuencial en un worker. Los resultados y tickets se conservan durante la sesión actual, no en almacenamiento persistente.
- No se incluyen pruebas automatizadas en el repositorio a esta fecha.
