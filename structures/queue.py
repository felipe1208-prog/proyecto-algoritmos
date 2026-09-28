from typing import Any, Optional, Generator
from structures.node import Node


class Queue:

    def __init__(self) -> None:
        self._front: Optional[Node] = None
        self._rear: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._front is None

    def size(self) -> int:
        return self._size

    def enqueue(self, data: Any) -> None:
        new_node = Node(data)
        if self.is_empty():
            self._front = new_node
            self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self) -> Optional[Any]:
        if self.is_empty():
            return None

        dequeued_node = self._front
        self._front = self._front.next
        dequeued_node.next = None
        self._size -= 1

        if self._front is None:
            self._rear = None

        return dequeued_node.data

    def peek(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._front.data

    def __iter__(self) -> Generator[Any, None, None]:
        current = self._front
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return self._size