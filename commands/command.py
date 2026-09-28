from abc import ABC, abstractmethod
from typing import List


class Command(ABC):

    @abstractmethod
    def execute(self, args: List[str]) -> None:
        pass