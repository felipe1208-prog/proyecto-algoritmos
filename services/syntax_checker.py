from typing import List, Tuple
from structures.stack import Stack
from models.diagnostic import Diagnostic


class SyntaxChecker:

    DELIMITER_PAIRS = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    OPENING_DELIMITERS = set("({[")
    CLOSING_DELIMITERS = set(")}]")

    @classmethod
    def check(cls, code: str) -> List[Diagnostic]:
        diagnostics: List[Diagnostic] = []
        stack: Stack = Stack()

        lines = code.splitlines()
        in_string_single = False
        in_string_double = False

        for line_num, line_text in enumerate(lines, start=1):
            col_num = 0
            while col_num < len(line_text):
                char = line_text[col_num]
                current_col = col_num + 1

                if char == "'" and not in_string_double:
                    in_string_single = not in_string_single
                    col_num += 1
                    continue
                if char == '"' and not in_string_single:
                    in_string_double = not in_string_double
                    col_num += 1
                    continue

                if not in_string_single and not in_string_double:
                    if char == "#" or (char == "/" and col_num + 1 < len(line_text) and line_text[col_num + 1] == "/"):
                        break

                    if char in cls.OPENING_DELIMITERS:
                        stack.push((char, line_num, current_col))

                    elif char in cls.CLOSING_DELIMITERS:
                        if stack.is_empty():
                            diagnostics.append(
                                Diagnostic(
                                    line=line_num,
                                    severity="CRITICAL",
                                    rule="SYNTAX_UNMATCHED_CLOSING",
                                    message=f"Delimitador de cierre '{char}' huérfano sin apertura previa.",
                                    column=current_col
                                )
                            )
                        else:
                            top_char, top_line, top_col = stack.pop()
                            expected_open = cls.DELIMITER_PAIRS[char]
                            if top_char != expected_open:
                                diagnostics.append(
                                    Diagnostic(
                                        line=line_num,
                                        severity="CRITICAL",
                                        rule="SYNTAX_MISMATCHED_PAIR",
                                        message=f"Discrepancia de delimitador: se esperaba cerrar '{top_char}' (de línea {top_line}:{top_col}), pero se encontró '{char}'.",
                                        column=current_col
                                    )
                                )

                col_num += 1

        while not stack.is_empty():
            unclosed_char, unclosed_line, unclosed_col = stack.pop()
            diagnostics.append(
                Diagnostic(
                    line=unclosed_line,
                    severity="CRITICAL",
                    rule="SYNTAX_UNCLOSED_DELIMITER",
                    message=f"Delimitador '{unclosed_char}' abierto nunca fue cerrado en el archivo.",
                    column=unclosed_col
                )
            )

        return diagnostics