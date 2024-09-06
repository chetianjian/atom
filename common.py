from typing import List, Dict
from singleton import Singleton
from test import AtomicList



def create(item):
    match item:
        case _ if isinstance(item, List):
            return AtomicList(item)
        case _ if isinstance(item, Dict):
            raise NotImplementedError
        case _ if isinstance(item, (Singleton, int, float)):
            return Singleton(item)
        case _:
            raise TypeError(f"Unknown data type: {type(item)}")