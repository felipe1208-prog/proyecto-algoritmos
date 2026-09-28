from typing import Any, Optional
from structures.node import Node


class Stack:

    def __init__(self) -> None:
        self._top: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._top is None

    def size(self) -> int:
        return self._size

    def push(self, data: Any) -> None:
        new_node = Node(data, next_node=self._top)
        self._top = new_node
        self._size += 1

    def pop(self) -> Optional[Any]:
        if self.is_empty():
            return None

        popped_node = self._top
        self._top = self._top.next
        popped_node.next = None  # Desconexión explícita
        self._size -= 1
        return popped_node.data

    def peek(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._top.data

    def clear(self) -> None:
        while not self.is_empty():
            self.pop()

    def __len__(self) -> int:
        return self._size