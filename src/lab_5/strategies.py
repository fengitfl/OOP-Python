from typing import Callable
from models import Patient, InpatientPatient, OutpatientPatient


# Стратегии сортировки (ключи для sorted)

def by_fio(patient: Patient) -> str:
    # Стратегия сортировки по ФИО (алфавитный порядок)
    return patient.fio


def by_age(patient: Patient) -> int:
    # Стратегия сортировки по возрасту
    return patient.age


def by_cost(patient: Patient) -> float:
    # Стратегия сортировки по стоимости лечения (требует метод calculate_cost)
    return patient.calculate_cost()


def by_record_number(patient: Patient) -> str:
    # Стратегия сортировки по номеру карты.
    return patient.record_number


def by_diagnosis_length(patient: Patient) -> int:
    # Стратегия сортировки по длине диагноза.
    return len(patient.diagnosis)


def by_multiple(patient: Patient) -> tuple:
    # Стратегия сортировки по нескольким атрибутам (сначала возраст, затем ФИО)
    return (patient.age, patient.fio)


# функции-фильтры (предикаты) 

def is_adult(patient: Patient) -> bool:
    # Фильтр: только взрослые пациенты (18+)
    return patient.age >= 18


def is_active(patient: Patient) -> bool:
    # Фильтр: только активные (не выписанные) пациенты
    return patient.is_active


def is_inpatient(patient: Patient) -> bool:
    # Фильтр: только стационарные пациенты.
    return isinstance(patient, InpatientPatient)


def is_outpatient(patient: Patient) -> bool:
    # Фильтр: только амбулаторные пациенты
    return isinstance(patient, OutpatientPatient)


def is_expensive(patient: Patient, threshold: float = 10000) -> bool:

    # Фильтр: пациенты со стоимостью лечения выше порога.
    # Используется с фабрикой.

    return patient.calculate_cost() > threshold


# Фабрики функций 
def make_age_filter(min_age: int, max_age: int) -> Callable:
#     Фабрика: создаёт фильтр по возрастному диапазону.
    def age_filter(patient: Patient) -> bool:
        return min_age <= patient.age <= max_age
    return age_filter


def make_cost_filter(max_cost: float) -> Callable:

    # Фабрика: создаёт фильтр по максимальной стоимости лечения.

    def cost_filter(patient: Patient) -> bool:
        return patient.calculate_cost() <= max_cost
    return cost_filter


def make_diagnosis_contains_filter(keyword: str) -> Callable:
    # Фабрика: создаёт фильтр по наличию ключевого слова в диагнозе.

    def diagnosis_filter(patient: Patient) -> bool:
        return keyword.lower() in patient.diagnosis.lower()
    return diagnosis_filter


# ФУНКЦИИ ДЛЯ map() (преобразования) 

def to_string(patient: Patient) -> str:
    # Преобразует пациента в строку (для map)
    return str(patient)


def extract_fio(patient: Patient) -> str:
    # Извлекает только ФИО
    return patient.fio


def extract_age(patient: Patient) -> int:
    # Извлекает возраст
    return patient.age


def apply_discount(discount_percent: float) -> Callable:

    # Фабрика: создаёт функцию для применения скидки к стоимости лечения.
    # Возвращает функцию, которая вычисляет новую стоимость.

    def discount_applier(patient: Patient) -> float:
        original_cost = patient.calculate_cost()
        return original_cost * (1 - discount_percent / 100)
    return discount_applier


# CALLABLE-ОБЪЕКТЫ (паттерн Стратегия) 

class DiscountStrategy:

    # Стратегия применения скидки как callable-объект.
    # Позволяет менять процент скидки без изменения кода коллекции.

    def __init__(self, discount_percent: float = 10.0):
        self.discount_percent = discount_percent
    
    def __call__(self, patient: Patient) -> float:
        # Возвращает стоимость лечения со скидкой
        return patient.calculate_cost() * (1 - self.discount_percent / 100)
    
    def set_discount(self, discount_percent: float):
        # Динамическое изменение стратегии.
        self.discount_percent = discount_percent


class PrintStrategy:
    # Стратегия печати информации о пациенте.
  def __call__(self, patient: Patient) -> None:
        # Используем имя класса вместо get_patient_type()
        patient_type = patient.__class__.__name__
        if patient_type == "Patient":
            patient_type = "Обычный пациент"
        elif patient_type == "InpatientPatient":
            patient_type = "Стационарный пациент"
        elif patient_type == "OutpatientPatient":
            patient_type = "Амбулаторный пациент"
        
        print(f" {patient_type}: {patient.fio}, "
              f"возраст: {patient.age}, диагноз: {patient.diagnosis}")


class UpgradeStrategy:
    # Стратегия "улучшения" пациента 
    def __call__(self, patient: Patient) -> None:
        if hasattr(patient, 'upgrade'):
            patient.upgrade()
        # Для простоты: если пациент активен, добавляем визит (для амбулаторных)
        if isinstance(patient, OutpatientPatient) and patient.is_active:
            patient.add_visit()