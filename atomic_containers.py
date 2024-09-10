from __future__ import annotations
from typing import Union, Iterable, List, Dict, Tuple, Set, Any, Hashable
from threading import Lock
from singleton import Singleton
from atomic import Atomic



def general_atomize(item: Any) -> Atomic:
    if isinstance(item, Atomic):
        return item
    TYPE_MAP = {list: AtomicList, 
                dict: AtomicDict, 
                tuple: AtomicTuple, 
                set: AtomicSet}
    return TYPE_MAP.get(type(item), Singleton)(item)



class AtomicList(Atomic):
    data: List[Atomic]
    lock: Lock

    def __init__(self, default: Union[AtomicList|List] = list()):
        assert isinstance(default, (AtomicList, List)), TypeError(f"default: {default} is not an AtomicList or List")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicList|List]) -> List:
        if isinstance(obj, AtomicList): 
            return obj.data
        else:
            return [general_atomize(item=item) for item in obj]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicList|Singleton]) -> bool:
        return value in self.data

    def __getitem__(self, index: int) -> Atomic:
        with self.data[index].lock:
            return self.data[index]

    def __setitem__(self, index: int, item: Any):
        with self.data[index].lock:
            self.data[index] = general_atomize(item=item)

    def __delitem__(self, index: int):
        with self.data[index].lock:
            del self.data[index]

    def __eq__(self, other: Any) -> bool:
        return self.data == other

    def extend(self, item: Union[AtomicList|List]):
        with self.lock:
            self.data.extend(self.atomize(obj=item))

    def append(self, item: Any):
        with self.lock:
            self.data.append(general_atomize(item=item))

    def remove(self, item: Any):
        with self.lock:
            self.data.remove(item)

    def count(self, item: Any) -> int:
        with self.lock:
            return self.data.count(item)

    def index(self, item: Any) -> int:
        with self.lock:
            return self.data.index(item)

    def pop(self, index: int) -> Any:
        with self.lock:
            return self.data.pop(index)

    def sort(self):
        with self.lock:
            self.data.sort()

    def reverse(self):
        with self.lock:
            self.data.reverse()

    def insert(self, index: int, item: Any):
        with self.lock:
            self.data.insert(index, item)



class AtomicDict(Atomic):
    data: Dict[Hashable, Atomic]
    lock: Lock

    def __init__(self, default: Union[AtomicDict|Dict] = dict()):
        assert isinstance(default, (AtomicDict, Dict)), TypeError(f"default: {default} is not an AtomicDict or Dict")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicDict|Dict]) -> Dict:
        if isinstance(obj, AtomicDict):
            return obj.data
        else:
            return {key: general_atomize(item=value) for key, value in obj.items()}

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicDict|Singleton]) -> bool:
        return value in self.data

    def __getitem__(self, key: Hashable) -> Atomic:
        with self.data[key].lock:
            return self.data[key]

    def __setitem__(self, key: Hashable, value: Any):
        with self.data.get(key, Singleton()).lock:
            self.data[key] = general_atomize(item=value)

    def __delitem__(self, key: Hashable):
        with self.data[key].lock:
            del self.data[key]

    def __eq__(self, other: Any) -> bool:
        return self.data == other

    def update(self, other: Union[AtomicDict|Dict]):
        with self.lock:
            self.data.update(self.atomize(other))

    def get(self, key: Hashable, default=None) -> Atomic:
        with self.data.get(key, Singleton()).lock:
            return self.data.get(key, default)

    def clear(self):
        with self.lock:
            self.data.clear()

    def pop(self, key: Hashable) -> Atomic:
        with self.data[key].lock:
            return self.data.pop(key)

    def keys(self):
        with self.lock:
            return self.data.keys()

    def values(self):
        with self.lock:
            return self.data.values()

    @classmethod
    def fromkeys(cls, arr: Iterable[Hashable], value: Any = None) -> AtomicDict:
        if not isinstance(value, Atomic):
            value = general_atomize(item=value)
        return cls(default=dict.fromkeys(arr, value))



class AtomicTuple(Atomic):
    data: Tuple[Atomic]
    lock: Lock

    def __init__(self, default: Union[AtomicTuple|Tuple] = tuple()):
        assert isinstance(default, (AtomicTuple, Tuple)), TypeError(f"default: {default} is not an AtomicTuple or Tuple")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicTuple|Tuple]) -> Tuple:
        if isinstance(obj, AtomicTuple):
            return obj.data
        else:
            return tuple([general_atomize(item=item) for item in obj])

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicTuple|Singleton]) -> bool:
        return value in self.data

    def __getitem__(self, key: int) -> Atomic:
        with self.data[key].lock:
            return self.data[key]

    def __eq__(self, other: Any) -> bool:
        return self.data == other

    def count(self, item: Atomic) -> int:
        with self.lock:
            return self.data.count(item)

    def index(self, item: Atomic) -> int:
        with self.lock:
            return self.data.index(item)



class AtomicSet(Atomic):
    data: Set[Singleton]
    lock: Lock

    def __init__(self, default: Union[AtomicSet|Set] = set()):
        assert isinstance(default, (AtomicSet, Set)), TypeError(f"default: {default} is not an AtomicSet or Set")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicSet|Set]) -> Set:
        if isinstance(obj, AtomicSet):
            return obj
        else:
            return set([Singleton(item) for item in obj])  # There is no nested set

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Any) -> bool:
        return value in self.data

    def __eq__(self, other: Any) -> bool:
        return self.data == other

    def add(self, item: Hashable):
        with self.lock:
            self.data.add(Singleton(item))

    def discard(self, item: Hashable):
        with self.lock:
            self.data.discard(item)

    def remove(self, item: Hashable):
        with self.lock:
            self.data.remove(Singleton(item))

    def pop(self) -> Singleton:
        with self.lock:
            return self.data.pop()

    def clear(self):
        with self.lock:
            self.data.clear()

    def difference(self, other: Union[Iterable|Hashable]) -> AtomicSet:
        with self.lock:
            return AtomicSet(self.data.difference(other))

    def difference_update(self, other: Union[Iterable|Hashable]):
        with self.lock:
            self.data.difference_update(other)

    def intersection(self, other: Union[Iterable|Hashable]) -> AtomicSet:
        with self.lock:
            return AtomicSet(self.data.intersection(other))

    def union(self, other: Union[Iterable|Hashable]) -> AtomicSet:
        with self.lock:
            return AtomicSet(self.data.union(other))

    def update(self, other: Union[Iterable|Hashable]):
        with self.lock:
            self.data.update(other)

    def isdisjoint(self, other: Union[Iterable|Hashable]) -> bool:
        with self.lock:
            return self.data.isdisjoint(other)

    def issubset(self, other: Union[Iterable|Hashable]) -> bool:
        with self.lock:
            return self.data.issubset(other)

    def issuperset(self, other: Union[Iterable|Hashable]) -> bool:
        with self.lock:
            return self.data.issuperset(other)



if __name__ == "__main__":
    import threading

    dic = AtomicDict({"a": 0, "b": 1, "c": 2})
    def f():
        global dic
        for i in range(1000000):
            dic["a"] += 1

    t1 = threading.Thread(target=f)
    t2 = threading.Thread(target=f)
    t1.start(), t2.start()
    t1.join(), t2.join()
    print(dic)


    lst = AtomicList([0, 1, 2])
    def g():
        global lst
        for i in range(1000000):
            lst[0] += 1
    t1 = threading.Thread(target=g)
    t2 = threading.Thread(target=g)
    t1.start(), t2.start()
    t1.join(), t2.join()
    print(lst)