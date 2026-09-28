from typing import Dict


class Diagnostic:

    SEVERITY_LEVELS: Dict[str, int] = {
        "CRITICAL": 3,
        "WARNING": 2,
        "INFO": 1,
    }

    def __init__(
        self,
        line: int,
        severity: str,
        rule: str,
        message: str,
        column: int = 1,
    ) -> None:
        self.line: int = line
        self.column: int = column
        self.severity: str = severity.upper() if severity.upper() in self.SEVERITY_LEVELS else "INFO"
        self.rule: str = rule
        self.message: str = message

    @property
    def severity_weight(self) -> int:
        return self.SEVERITY_LEVELS.get(self.severity, 0)

    def __repr__(self) -> str:
        return (
            f"Diagnostic(line={self.line}, col={self.column}, "
            f"severity='{self.severity}', rule='{self.rule}', message='{self.message}')"
        )

    def __str__(self) -> str:
        return f"[{self.severity}] Línea {self.line}:{self.column} ({self.rule}) -> {self.message}"