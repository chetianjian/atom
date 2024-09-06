from __future__ import annotations
from typing import Union
from atomic import Atomic
from threading import Lock



class Singleton(Atomic):
    data: Union[int|float]
    lock: Lock

    def __init__(self, default: Union[Singleton|int|float]):
        super().__init__(default)

    @staticmethod
    def atomize(obj):
        if isinstance(obj, Singleton):
            return obj.data
        else:
            return obj

    def __eq__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return self.data == other.data
        else:
            return self.data == other

    def __ne__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return self.data != other.data
        else:
            return self.data != other

    def __lt__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return self.data < other.data
        else:
            return self.data < other

    def __le__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return self.data <= other.data
        else:
            return self.data <= other

    def __gt__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return self.data > other.data
        else:
            return self.data > other

    def __ge__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return self.data >= other.data
        else:
            return self.data >= other

    def __add__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data + other.data)
        else:
            return Singleton(self.data + other)

    def __sub__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data - other.data)
        else:
            return Singleton(self.data + other)

    def __mul__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data * other.data)
        else:
            return Singleton(self.data + other)

    def __truediv__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data / other.data)
        else:
            return Singleton(self.data / other)

    def __floordiv__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data // other.data)
        else:
            return Singleton(self.data // other)

    def __mod__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data % other.data)
        else:
            return Singleton(self.data % other)

    def __pow__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(self.data ** other.data)
        else:
            return Singleton(self.data ** other)

    def __radd__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data + self.data)
        else:
            return Singleton(other + self.data)

    def __rsub__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data - self.data)
        else:
            return Singleton(other - self.data)

    def __rmul__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data * self.data)
        else:
            return Singleton(other * self.data)

    def __rtruediv__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data / self.data)
        else:
            return Singleton(other / self.data)

    def __rfloordiv__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data // self.data)
        else:
            return Singleton(other // self.data)

    def __rmod__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data % self.data)
        else:
            return Singleton(other % self.data)
        
    def __rpow__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            return Singleton(other.data ** self.data)
        else:
            return Singleton(other ** self.data)

    def __iadd__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data += other.data
        else:
            with self.lock:
                self.data += other
        return self

    def __isub__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data -= other.data
        else:
            with self.lock:
                self.data -= other
        return self

    def __imul__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data *= other.data
        else:
            with self.lock:
                self.data *= other
        return self

    def __itruediv__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data /= other.data
        else:
            with self.lock:
                self.data /= other
        return self

    def __ifloordiv__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data //= other.data
        else:
            with self.lock:
                self.data // other
        return self

    def __imod__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data %= other.data
        else:
            with self.lock:
                self.data %= other
        return self

    def __ipow__(self, other: Union[Singleton|int|float]):
        if other.__class__ is Singleton:
            with self.lock:
                self.data **= other.data
        else:
            with self.lock:
                self.data **= other
        return self

    def __int__(self):
        return int(self.data)

    def __float__(self):
        return float(self.data)

    def __complex__(self): 
        return complex(self.data)

    def get(self):
        with self.lock:
            return self.data

    def set(self, value: Union[int|float]):
        with self.lock:
            self.data = value



if __name__ == "__main__":
    obj = Singleton(0)
    import threading
    def f():
        global obj
        for i in range(1000000):
            with obj.lock:
                obj += 1

    t1 = threading.Thread(target=f)
    t2 = threading.Thread(target=f)
    t1.start(), t2.start()
    t1.join(), t2.join()
    print(obj)
    