from typing import List
from models.diagnostic import Diagnostic
from services.syntax_checker import SyntaxChecker


class StaticAnalyzer:

    def __init__(self, max_line_length: int = 80) -> None:
        self.max_line_length: int = max_line_length

    def analyze(self, code: str) -> List[Diagnostic]:
        diagnostics: List[Diagnostic] = []

        if not code or not code.strip():
            diagnostics.append(
                Diagnostic(
                    line=1,
                    severity="INFO",
                    rule="EMPTY_BUFFER",
                    message="El archivo está completamente vacío.",
                    column=1
                )
            )
            return diagnostics

        syntax_issues = SyntaxChecker.check(code)
        for issue in syntax_issues:
            diagnostics.append(issue)

        lines = code.splitlines()
        empty_lines_count = 0

        for line_num, line in enumerate(lines, start=1):
            line_len = len(line)

            if line_len > self.max_line_length:
                diagnostics.append(
                    Diagnostic(
                        line=line_num,
                        severity="WARNING",
                        rule="LINE_LENGTH_EXCEEDED",
                        message=f"La línea supera los {self.max_line_length} caracteres permitidos ({line_len} caracteres).",
                        column=self.max_line_length + 1
                    )
                )

            if line.endswith(" ") or line.endswith("\t"):
                diagnostics.append(
                    Diagnostic(
                        line=line_num,
                        severity="INFO",
                        rule="TRAILING_WHITESPACE",
                        message="Línea con espacios o tabulaciones residuales al final.",
                        column=line_len
                    )
                )

            if not line.strip():
                empty_lines_count += 1
                if empty_lines_count >= 3:
                    diagnostics.append(
                        Diagnostic(
                            line=line_num,
                            severity="INFO",
                            rule="EXCESSIVE_BLANK_LINES",
                            message="Bloque con más de dos líneas en blanco consecutivas.",
                            column=1
                        )
                    )
            else:
                empty_lines_count = 0

            leading_spaces = len(line) - len(line.lstrip(" "))
            if leading_spaces >= 16:
                diagnostics.append(
                    Diagnostic(
                        line=line_num,
                        severity="WARNING",
                        rule="HIGH_NESTING_LEVEL",
                        message=f"Profundidad de indentación elevada ({leading_spaces} espacios). Considere modularizar.",
                        column=leading_spaces
                    )
                )

        return diagnostics