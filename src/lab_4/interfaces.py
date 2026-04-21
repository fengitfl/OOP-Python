from abc import ABC, abstractmethod

class Treatable(ABC):

    @abstractmethod
    def calculate_cost(self):
        pass

class Diagnosable(ABC):

    @abstractmethod
    def get_diagnosis_info(self):
        pass

class Comparable(ABC):

    @abstractmethod
    def compare_to(self, other):
        pass