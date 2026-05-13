
from datetime import date
from collection import PatientCollection
from models import Patient, InpatientPatient, OutpatientPatient
from strategies import (
    by_fio, by_age, by_cost, by_record_number, by_multiple,
    is_adult, is_active, is_inpatient, is_outpatient,
    make_age_filter, make_cost_filter, make_diagnosis_contains_filter,
    to_string, extract_fio, extract_age, apply_discount,
    DiscountStrategy, PrintStrategy
)


def create_test_collection() -> PatientCollection:
    collection = PatientCollection()
    
    # Обычные пациенты
    p1 = Patient("Алексеев Дмитрий", 30, "Здоров", "004")
    p2 = Patient("Иванов Иван", 45, "Гипертония", "001")
    
    # Стационарные пациенты
    p3 = InpatientPatient("Петрова Анна", 68, "Пневмония", "002", ward=302, daily_rate=5500)
    p3.add_days(7)  # 7 дней в стационаре
    
    p4 = InpatientPatient("Морозова Елена", 55, "Гастрит", "005", ward=101, daily_rate=4000)
    p4.add_days(3)  # 3 дня
    
    # Амбулаторные пациенты
    p5 = OutpatientPatient("Сидоров Олег", 20, "Мигрень", "003",
                           next_appointment=date(2026, 5, 15),
                           attending_doctor="Доктор Хаус",
                           consultation_price=2500)
    p5.add_visit()
    p5.add_visit()
    p5.add_visit()  # 3 визита
    
    p6 = OutpatientPatient("Козлова Мария", 35, "Ангина", "006",
                           consultation_price=1500)
    p6.add_visit()
    
    collection.add_all([p1, p2, p3, p4, p5, p6])
    return collection


def print_collection(collection: PatientCollection, title: str):
    print(f"\n{'=' * 60}")
    print(f"📊 {title}")
    print('=' * 60)
    for i, patient in enumerate(collection.get_all(), 1):
        cost = patient.calculate_cost()
        print(f"{i}. {patient.fio:30} | {patient.age:3} лет | "
              f"диагноз: {patient.diagnosis:20} | стоимость: {cost:>8.0f} руб.")


def demo_level3():
    print("=== Сортировки и фильтры === ")
    
    collection = create_test_collection()
    
    # 1. Сортировка по ФИО
    print_collection(collection.sort_by(by_fio), "Сортировка по ФИО (алфавит)")
    
    # 2. Сортировка по возрасту
    print_collection(collection.sort_by(by_age), "Сортировка по возрасту (младшие → старшие)")
    
    # 3. Сортировка по стоимости лечения
    print_collection(collection.sort_by(by_cost, reverse=True), 
                     "Сортировка по стоимости лечения (дорогие → дешёвые)")
    
    # 4. Фильтр: только взрослые пациенты
    adults = collection.filter_by(is_adult)
    print_collection(adults, "Фильтр: только взрослые пациенты (18+)")
    
    # 5. Фильтр: только активные пациенты
    active = collection.filter_by(is_active)
    print_collection(active, "Фильтр: только активные пациенты")


def demo_level4():
    print(" === map(), фабрики функций, методы коллекции ===")
    
    collection = create_test_collection()
    
    print("\n map(): преобразование пациентов в строки")
    strings = collection.map(to_string)
    for s in strings[:3]:
        print(f"   {s[:80]}...")

    print("\n map(): извлечение ФИО всех пациентов")
    names = collection.map(extract_fio)
    print(f"   Список ФИО: {names}")
    
    print("\n Фабрика функций: применение скидки 20%")
    discount_func = apply_discount(20)
    discounted_costs = collection.map(discount_func)
    for patient, new_cost in zip(collection.get_all(), discounted_costs):
        old_cost = patient.calculate_cost()
        print(f"   {patient.fio}: {old_cost:.0f} руб → {new_cost:.0f} руб (скидка 20%)")
    

    print("\n Фабрика фильтров: пациенты от 30 до 50 лет")
    age_filter = make_age_filter(30, 50)
    age_filtered = collection.filter_by(age_filter)
    print_collection(age_filtered, "Возраст 30–50 лет")
    

    print("\n Фабрика фильтров: пациенты с диагнозом, содержащим 'и'")
    diagnosis_filter = make_diagnosis_contains_filter("и")
    diag_filtered = collection.filter_by(diagnosis_filter)
    print_collection(diag_filtered, "Диагноз содержит букву 'и'")
    
    print("\n Методы коллекции: filter_by → sort_by (цепочка)")
    result = (collection
              .filter_by(is_inpatient)
              .sort_by(by_cost, reverse=True))
    print_collection(result, "Стационарные пациенты, сортировка по стоимости (дорогие сверху)")
    
    print("\n Сравнение: lambda vs именованная функция")
    print("   Сортировка через lambda:")
    lambda_sorted = PatientCollection(collection.get_all()).sort_by(lambda p: p.age)
    for p in lambda_sorted.get_all():
        print(f"      {p.fio}: {p.age} лет")
    
    print("   Сортировка через именованную функцию by_age:")
    named_sorted = PatientCollection(collection.get_all()).sort_by(by_age)
    for p in named_sorted.get_all():
        print(f"      {p.fio}: {p.age} лет")


def demo_level5():
    print("=== Паттерн Стратегия, callable-объекты, цепочки ===")

    
    collection = create_test_collection()
    
    print("\n Callable-стратегия: Применение скидки")
    discount_strategy = DiscountStrategy(discount_percent=15)
    for patient in collection.get_all():
        new_cost = discount_strategy(patient)
        old_cost = patient.calculate_cost()
        print(f"   {patient.fio}: {old_cost:.0f} руб → {new_cost:.0f} руб (скидка 15%)")
    
    print("\n Смена стратегии: изменение процента скидки")
    discount_strategy.set_discount(30)
    for patient in collection.get_all():
        if patient.calculate_cost() > 0:
            new_cost = discount_strategy(patient)
            old_cost = patient.calculate_cost()
            print(f"   {patient.fio}: {old_cost:.0f} руб → {new_cost:.0f} руб (скидка 30%)")
    

    print("\n Метод apply(): применение стратегии печати")
    print_strategy = PrintStrategy()
    collection.apply(print_strategy)
    
    print("\n Цепочка операций: фильтрация → сортировка → применение → преобразование")
    
    def activate_patient(patient):
        if not patient.is_active:
            patient.reinstate()
    
    # Цепочка
    result = (PatientCollection(collection.get_all())
              .filter_by(is_outpatient)           # только амбулаторные
              .sort_by(by_cost, reverse=True)     # по стоимости (дорогие сверху)
              .apply(lambda p: print(f"   Обработан: {p.fio}"))  # вывод
              )
    
    print_collection(result, "Результат цепочки: амбулаторные пациенты")
    
    # 5. Сложная цепочка с reduce и map
    print("\n Анализ коллекции через цепочки:")
    
    total_cost = (PatientCollection(collection.get_all())
                  .map(lambda p: p.calculate_cost())
                  .reduce(lambda a, b: a + b, 0))
    print(f"    Общая стоимость лечения всех пациентов: {total_cost:.0f} руб.")
    
    # Средний возраст
    avg_age = (PatientCollection(collection.get_all())
               .map(extract_age)
               .reduce(lambda a, b: a + b, 0) / len(collection))
    print(f"   📊 Средний возраст пациентов: {avg_age:.1f} лет")
    
    # 6. Демонстрация взаимозаменяемости стратегий
    print("\n📌 Взаимозаменяемость стратегий (без изменения кода коллекции):")
    sorted_by_age = PatientCollection(collection.get_all()).sort_by(by_age)
    print("   Стратегия 1 (по возрасту):")
    for p in sorted_by_age.get_all()[:3]:
        print(f"      {p.fio}: {p.age} лет")
    
    sorted_by_fio = PatientCollection(collection.get_all()).sort_by(by_fio)
    print("   Стратегия 2 (по ФИО):")
    for p in sorted_by_fio.get_all()[:3]:
        print(f"      {p.fio}: {p.age} лет")
    
    sorted_by_cost = PatientCollection(collection.get_all()).sort_by(by_cost)
    print("   Стратегия 3 (по стоимости лечения):")
    for p in sorted_by_cost.get_all()[:3]:
        print(f"      {p.fio}: {p.calculate_cost():.0f} руб")


def main():
    print(" ЛАБОРАТОРНАЯ РАБОТА №5".center(70))
    print(" Функции как аргументы. Стратегии и делегаты".center(70))
    
    demo_level3()
    demo_level4()
    demo_level5()
    
if __name__ == "__main__":
    main()