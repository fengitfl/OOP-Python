from abc import ABC, abstractmethod
from typing import Any

class Printable(ABC):
    @abstractmethod
    def to_string(self) -> str:
        # Возвращает строковое представление объекта для вывода
        pass


class Comparable(ABC):
    @abstractmethod
    def compare_to(self, other: Any) -> int:

        pass

class CostCalculable(ABC):   
    @abstractmethod
    def calculate_cost(self) -> float:
        # Возвращает стоимость лечения пациента
        pass


class Diagnosable(ABC):
    #Интерфейс для объектов, предоставляющих информацию о диагнозе
    @abstractmethod
    def get_diagnosis_info(self) -> str:
# Возвращает информацию о диагнозе
        pass


class Treatable(ABC):
# Интерфейс для объектов, которые можно лечить/назначать лечение

    @abstractmethod
    def can_prescribe_medicine(self) -> bool:
        # Можно ли назначить лекарства
        pass