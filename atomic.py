from threading import Lock
from abc import ABC, abstractmethod
from typing import Iterable



class Atomic(ABC):
    def __init__(self, default):
        self.data = self.atomize(default)
        self.lock = Lock()

    @abstractmethod
    def atomize(obj):
        raise NotImplementedError("staticmethod `atomize` not implemented")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"
    
    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

