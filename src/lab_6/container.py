from typing import TypeVar, Generic, Callable, Optional, List, Iterator, Protocol, runtime_checkable
from functools import reduce as functools_reduce

T = TypeVar('T')          # Тип элементов коллекции
R = TypeVar('R')          # Тип результата для map() и reduce()


# GENERIC COLLECTION 
class TypedCollection(Generic[T]):
    # Generic-версия коллекции для хранения элементов типа T
    # Поддерживает основные методы работы с коллекцией


    def __init__(self, items: Optional[List[T]] = None) -> None:
        self._items: List[T] = list(items) if items else []

    def add(self, item: T) -> None:
        # Добавляет один элемент
        self._items.append(item)

    def add_all(self, items: List[T]) -> None:
        # Добавляет несколько элементов
        self._items.extend(items)

    def remove(self, item: T) -> None:
        # Удаляет элемент (если есть)
        self._items.remove(item)

    def get_all(self) -> List[T]:
        # Возвращает копию списка элементов
        return self._items.copy()

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        # Возвращает первый элемент, удовлетворяющий условию
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        # Возвращает список всех элементов, удовлетворяющих условию
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> List[R]:
        # Применяет функцию преобразования к каждому элементу
        return [transform(item) for item in self._items]

    def reduce(self, func: Callable[[R, T], R], initial: R) -> R:
        
        # Сворачивает коллекцию с начальным значением
        # func(аккумулятор, элемент) -> новый_аккумулятор
        # Тип аккумулятора (R) может отличаться от типа элементов (T)
         return functools_reduce(func, self._items, initial)

    def sort_by(self, key_func: Callable[[T], any], reverse: bool = False) -> 'TypedCollection[T]':
        # Сортирует коллекцию и возвращает себя (для цепочек)
        self._items.sort(key=key_func, reverse=reverse)
        return self

    def __str__(self) -> str:
        return f"TypedCollection({len(self._items)} items)"


#  PROTOCOLS 
@runtime_checkable
class Displayable(Protocol):
    # Протокол: объект должен иметь метод display() -> str
    def display(self) -> str:
        ...

@runtime_checkable
class Scorable(Protocol):
    # Протокол: объект должен иметь метод score() -> float
    def score(self) -> float:
        ...


# TypeVar с ограничением (bound) – только для типов, реализующих протокол
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)


# Специализированные типы коллекций
DisplayableCollection = TypedCollection[D]
ScorableCollection = TypedCollection[S]