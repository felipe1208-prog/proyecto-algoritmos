from typing import Any, Optional, Generator
from structures.node import Node


class LinkedList:

    def __init__(self) -> None:
        self._head: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._head is None

    def size(self) -> int:
        return self._size

    def append(self, data: Any) -> None:
        new_node = Node(data)
        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def get_at(self, index: int) -> Optional[Any]:
        if index < 0 or index >= self._size:
            return None

        current = self._head
        for _ in range(index):
            if current is None:
                return None
            current = current.next

        return current.data if current else None

    def delete_by_predicate(self, predicate) -> Optional[Any]:
        if self._head is None:
            return None

        if predicate(self._head.data):
            deleted_data = self._head.data
            self._head = self._head.next
            self._size -= 1
            return deleted_data

        current = self._head
        while current.next is not None:
            if predicate(current.next.data):
                deleted_data = current.next.data
                current.next = current.next.next
                self._size -= 1
                return deleted_data
            current = current.next

        return None

    def find_by_predicate(self, predicate) -> Optional[Any]:
        current = self._head
        while current is not None:
            if predicate(current.data):
                return current.data
            current = current.next
        return None

    def __iter__(self) -> Generator[Any, None, None]:
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return self._size