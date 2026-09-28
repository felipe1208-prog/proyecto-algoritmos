from typing import List, Generator
from structures.stack import Stack


class CodeFile:

    def __init__(self, name: str, initial_content: str = "") -> None:
        self.name: str = name
        self.content: str = initial_content
        self._undo_stack: Stack = Stack()
        self._redo_stack: Stack = Stack()

    def update_content(self, new_content: str, record_history: bool = True) -> None:
        if record_history and new_content != self.content:
            self._undo_stack.push(self.content)
            self._redo_stack.clear()
        self.content = new_content

    def undo(self) -> bool:
        if self._undo_stack.is_empty():
            return False

        previous_state = self._undo_stack.pop()
        self._redo_stack.push(self.content)
        self.content = previous_state
        return True

    def redo(self) -> bool:
        if self._redo_stack.is_empty():
            return False

        future_state = self._redo_stack.pop()
        self._undo_stack.push(self.content)
        self.content = future_state
        return True

    def get_lines(self) -> List[str]:
        if not self.content:
            return []
        return self.content.splitlines()

    def line_count(self) -> int:
        if not self.content:
            return 0
        return len(self.content.splitlines())

    def undo_depth(self) -> int:
        return self._undo_stack.size()

    def redo_depth(self) -> int:
        return self._redo_stack.size()

    def __repr__(self) -> str:
        return f"CodeFile(name='{self.name}', lines={self.line_count()})"