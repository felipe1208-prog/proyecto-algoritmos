from typing import List
from models.diagnostic import Diagnostic


class MergeSort:

    @classmethod
    def sort(cls, items: List[Diagnostic], criterion: str = "line") -> List[Diagnostic]:
        if items is None:
            return []

        elements: List[Diagnostic] = [item for item in items]
        if len(elements) <= 1:
            return elements

        cls._merge_sort_recursive(elements, criterion.lower())
        return elements

    @classmethod
    def _merge_sort_recursive(cls, arr: List[Diagnostic], criterion: str) -> None:
        if len(arr) > 1:
            mid = len(arr) // 2

            left_half = [arr[i] for i in range(0, mid)]
            right_half = [arr[i] for i in range(mid, len(arr))]

            cls._merge_sort_recursive(left_half, criterion)
            cls._merge_sort_recursive(right_half, criterion)

            i = 0
            j = 0
            k = 0

            while i < len(left_half) and j < len(right_half):
                if cls._compare(left_half[i], right_half[j], criterion) <= 0:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1

    @staticmethod
    def _compare(a: Diagnostic, b: Diagnostic, criterion: str) -> int:
        if criterion in ("gravedad", "severity"):
            if a.severity_weight != b.severity_weight:
                return -1 if a.severity_weight > b.severity_weight else 1
            
            return -1 if a.line < b.line else (1 if a.line > b.line else 0)

        if a.line != b.line:
            return -1 if a.line < b.line else 1
        
        return -1 if a.column < b.column else (1 if a.column > b.column else 0)