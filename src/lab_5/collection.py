from typing import List, Callable, TypeVar

T = TypeVar('T')


class PatientCollection:

    def __init__(self, items: List = None):
        self._items = list(items) if items else []
    
    def add(self, item):
        self._items.append(item)
        return self
    
    def add_all(self, items: List):
        self._items.extend(items)
        return self
    
    def get_all(self) -> List:
        return self._items.copy()
    
    def sort_by(self, key_func: Callable, reverse: bool = False):
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate: Callable):
        filtered = list(filter(predicate, self._items))
        return PatientCollection(filtered)
    
    def apply(self, func: Callable):
        for item in self._items:
            func(item)
        return self
    
    def map(self, transform_func: Callable) -> 'PatientCollection':
 
        transformed = list(map(transform_func, self._items))
        return PatientCollection(transformed)
    
    def reduce(self, func: Callable, initial=None):
        from functools import reduce
        if initial is None:
            return reduce(func, self._items)
        return reduce(func, self._items, initial)
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __getitem__(self, index) -> object:
        return self._items[index]
    
    def __iter__(self):
        return iter(self._items)
    
    def __str__(self) -> str:
        return f"PatientCollection({len(self._items)} items)"
    
    def __repr__(self) -> str:
        return f"PatientCollection({self._items!r})"