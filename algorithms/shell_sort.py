from typing import List
from models.diagnostic import Diagnostic


class ShellSort:

    @classmethod
    def sort(cls, items: List[Diagnostic], criterion: str = "line") -> List[Diagnostic]:
        if items is None:
            return []

        arr: List[Diagnostic] = [item for item in items]
        n = len(arr)
        if n <= 1:
            return arr

        crit = criterion.lower()
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and cls._compare(arr[j - gap], temp, crit) > 0:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2

        return arr

    @staticmethod
    def _compare(a: Diagnostic, b: Diagnostic, criterion: str) -> int:
        if criterion in ("gravedad", "severity"):
            if a.severity_weight != b.severity_weight:
                return -1 if a.severity_weight > b.severity_weight else 1
            return -1 if a.line < b.line else (1 if a.line > b.line else 0)

        if a.line != b.line:
            return -1 if a.line < b.line else 1
        return -1 if a.column < b.column else (1 if a.column > b.column else 0)