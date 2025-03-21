from threading import Lock
from abc import ABC, abstractmethod



class Atomic(ABC):
    def __init__(self, default):
        self.data = self.atomize(default)
        self.lock = Lock()

    @abstractmethod
    def atomize(obj):
        raise NotImplementedError("staticmethod `atomize` is not implemented")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"
