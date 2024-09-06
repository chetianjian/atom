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
    


