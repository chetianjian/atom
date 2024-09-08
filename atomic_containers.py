from __future__ import annotations
from typing import Union, Iterable, List, Dict, Tuple, Set
from threading import Lock
from singleton import Singleton
from atomic import Atomic



class AtomicList(Atomic):
    data: List[AtomicList|Singleton]
    lock: Lock

    def __init__(self, default: Union[AtomicList|List[AtomicList|List|Singleton|int|float]]):
        assert isinstance(default, (AtomicList, List)), TypeError(f"default: {default} is not an AtomicList or List")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicList|List[AtomicList|List|Singleton|int|float]]) -> List:
        if isinstance(obj, AtomicList):
            atomized_list: List = obj.data
        else:
            atomized_list: List = list()
            for item in obj:
                if isinstance(item, Iterable):
                    atomized_list.append(AtomicList.atomize(obj=item))
                else:
                    atomized_list.append(Singleton(item))
        return atomized_list

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicList|Singleton]) -> bool:
        return value in self.data

    def __getitem__(self, index: int) -> Atomic:
        with self.data[index].lock:
            return self.data[index]

    def __setitem__(self, index: int, item: Union[Atomic|int|float]):
        if isinstance(item, Atomic):
            with self.data[index].lock:
                self.data[index] = item
        else:
            with self.data[index].lock:
                self.data[index] = Singleton(item)

    def __delitem__(self, index: int):
        with self.data[index].lock:
            del self.data[index]

    def __eq__(self, other: Union[AtomicList|List]):
        if isinstance(other, AtomicList):
            return self.data == other.data
        else:
            return self.data == other

    def extend(self, other: Union[AtomicList|List[Singleton|int|float]]):
        with self.lock:
            atomized_list = self.atomize(obj=other)
            self.data.extend(atomized_list)

    def append(self, other: Union[AtomicList|List|Singleton|int|float]):
        if isinstance(other, (AtomicList, List)):
            with self.lock:
                self.data.append(AtomicList(other))
        else:
            with self.lock:
                self.data.append(Singleton(other))

    def remove(self, item: Atomic):
        for _ in range(len(self)):
            if self.data[_] == item:
                with self.data[_].lock:
                    del self.data[_]
                break

    def count(self, item: Atomic):
        with self.lock:
            return self.data.count(item)

    def index(self, item: Atomic):
        with self.lock:
            return self.data.index(item)

    def pop(self, index: int) -> Atomic:
        with self.lock:
            return self.data.pop(index)

    def sort(self):
        with self.lock:
            self.data.sort()

    def reverse(self):
        with self.lock:
            self.data.reverse()

    def insert(self, index: int, item: Union[Atomic|int|float]):
        with self.lock:
            self.data.insert(index, item)



class AtomicDict(Atomic):
    data: Dict[str, AtomicDict|Singleton]
    lock: Lock

    def __init__(self, default: Union[AtomicDict|Dict[str, AtomicDict|Dict|Singleton|int|float]]):
        assert isinstance(default, (AtomicDict, Dict)), TypeError(f"default: {default} is not an AtomicDict or Dict")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicDict|Dict[str, AtomicDict|Dict|Singleton|int|float]]) -> Dict:
        if isinstance(obj, AtomicDict):
            atomized_dict: Dict = obj.data
        else:
            atomized_dict = dict()
            for key, value in obj.items():
                if isinstance(value, Iterable):
                    atomized_dict[key] = AtomicDict.atomize(obj=value)
                else:
                    atomized_dict[key] = Singleton(value)
        return atomized_dict

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicDict|Singleton]) -> bool:
        return value in self.data

    def __getitem__(self, key: str) -> Atomic:
        with self.data[key].lock:
            return self.data[key]

    def __setitem__(self, key: str, value: Union[AtomicDict|Dict|Singleton|int|float]):
        if isinstance(value, (AtomicDict, Dict)):
            with self.data[key].lock:
                self.data[key] = AtomicDict(value)
        else:
            with self.data[key].lock:
                self.data[key] = Singleton(value)

    def __delitem__(self, key: str):
        with self.data[key].lock:
            del self.data[key]

    def __eq__(self, other: Union[AtomicDict|Dict]):
        if isinstance(other, AtomicDict):
            return self.data == other.data
        else:
            return self.data == other

    def update(self, other: Union[AtomicDict|Dict]):
        with self.lock:
            self.data.update(self.atomize(other))

    def get(self, key: str) -> Atomic:
        with self.data[key].lock:
            return self.data[key]

    def clear(self):
        with self.lock:
            self.data = dict()
            self.lock = Lock()

    def pop(self, key: str) -> Atomic:
        with self.data[key].lock:
            return self.data.pop(key)

    def keys(self):
        with self.lock:
            return self.data.keys()

    def values(self):
        with self.lock:
            return self.data.values()

    @classmethod
    def fromkeys(cls, arr: Iterable[str], value: Union[Atomic|int|float]):
        if not isinstance(value, Atomic):
            value = Singleton(value)
        return cls.__init__(dict.fromkeys(arr, value))



class AtomicTuple(Atomic):
    data: Tuple[AtomicTuple|Singleton]
    lock: Lock
    
    def __init__(self, default: Union[AtomicTuple|Tuple[AtomicList|List|Singleton|int|float]]):
        assert isinstance(default, (AtomicTuple, Tuple)), TypeError(f"default: {default} is not an AtomicTuple or Tuple")
        super().__init__(default=default)
        
    @staticmethod
    def atomize(obj: Union[AtomicTuple|Tuple[AtomicTuple|Tuple|Singleton|int|float]]) -> Tuple:
        if isinstance(obj, AtomicTuple):
            atomized_tuple: Tuple = obj.data
        else:
            arr: List = list()
            for item in obj:
                if isinstance(item, Iterable):
                    arr.append(AtomicTuple.atomize(obj=item))
                else:
                    arr.append(Singleton(item))
            atomized_tuple = tuple(arr)
        return atomized_tuple

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicTuple|Singleton]) -> bool:
        return value in self.data

    def __getitem__(self, key: int) -> Atomic:
        with self.data[key].lock:
            return self.data[key]

    def __eq__(self, other: Union[AtomicTuple|Tuple]):
        if isinstance(other, AtomicTuple):
            return self.data == other.data
        else:
            return self.data == other

    def count(self, item: Atomic):
        with self.lock:
            return self.data.count(item)

    def index(self, item: Atomic):
        with self.lock:
            return self.data.index(item)



class AtomicSet(Atomic):
    data: Set[AtomicSet|Singleton]
    lock: Lock
    
    def __init__(self, default: Union[AtomicSet|Set[AtomicSet|Set|Singleton|int|float]]):
        assert isinstance(default, (AtomicSet, Set)), TypeError(f"default: {default} is not an AtomicSet or Set")
        super().__init__(default=default)

    @staticmethod
    def atomize(obj: Union[AtomicSet|Set[AtomicSet|Set|Singleton|int|float]]) -> Set:
        if isinstance(obj, AtomicTuple):
            atomized_set: Set = obj.data
        else:
            atomized_set = set()
            for item in obj:
                if isinstance(item, Iterable):
                    atomized_set.add(AtomicSet.atomize(obj=item))
                else:
                    atomized_set.add(Singleton(item))
        return atomized_set

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable:
        return iter(self.data)

    def __contains__(self, value: Union[AtomicSet|Singleton]) -> bool:
        return value in self.data

    def __eq__(self, other: Union[AtomicSet|Set]):
        if isinstance(other, AtomicSet):
            return self.data == other.data
        else:
            return self.data == other







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
