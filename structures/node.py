from typing import Any, Optional


class Node:
    
    def __init__(self, data: Any, next_node: Optional["Node"] = None) -> None:
        self.data: Any = data
        self.next: Optional["Node"] = next_node

    def __repr__(self) -> str:
        return f"Node(data={self.data})"