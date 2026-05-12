# demo.py
from datetime import date
from base import Patient, InpatientPatient, OutpatientPatient
from container import TypedCollection, Displayable, Scorable


def create_patients() -> list[Patient]:
    # Обычные пациенты
    p1 = Patient("Алексеев Дмитрий", 30, "Здоров", "004")
    p2 = Patient("Иванов Иван", 45, "Гипертония", "001")
    
    # Стационарный пациент
    p3 = InpatientPatient("Петрова Анна", 68, "Пневмония", "002", ward=302, daily_rate=5500)
    p3.add_days(7)
    p4 = InpatientPatient("Морозова Елена", 55, "Гастрит", "005", ward=101, daily_rate=4000)
    p4.add_days(3)
    
    # Амбулаторные пациенты
    p5 = OutpatientPatient("Сидоров Олег", 20, "Мигрень", "003",
                           next_appointment=date(2026, 5, 15),
                           attending_doctor="Доктор Хаус",
                           consultation_price=2500)
    p5.add_visit()
    p5.add_visit()
    p5.add_visit()
    
    p6 = OutpatientPatient("Козлова Мария", 35, "Ангина", "006",
                           consultation_price=1500)
    p6.add_visit()
    p6.add_visit()
    
    return [p1, p2, p3, p4, p5, p6]


def demo_level3() -> None:
    print("==== Generic-коллекция TypedCollection ==== ")
    
    # Создаём типизированную коллекцию
    coll = TypedCollection[Patient]()
    patients = create_patients()
    coll.add_all(patients)
    
    print(f"Создана коллекция с {len(coll)} пациентами.")
    print("\n Список пациентов (через display()):")
    for i, patient in enumerate(coll.get_all(), 1):
        print(f"   {i}. {patient.display()}")
    
    # Демонстрация итератора
    print("\n Итерация по коллекции:")
    for patient in coll:
        print(f"   - {patient.fio}, {patient.age} лет")


def demo_level4() -> None:
    # демонстрация find, filter, map.
    print("==== find, filter, map ==== ")
    
    coll = TypedCollection[Patient]()
    patients = create_patients()
    coll.add_all(patients)
    
    # 1. find() - элемент найден
    print("\n Поиск пациента старше 60 лет (find):")
    found = coll.find(lambda p: p.age > 60)
    if found:
        print(f"   Найден: {found.display()}")
    
    # 2. find() - элемент не найден
    print("\n Поиск пациента старше 100 лет (find):")
    not_found = coll.find(lambda p: p.age > 100)
    print(f"   Результат: {not_found}")
    
    # 3. filter() - отбор взрослых пациентов
    print("\n Фильтр: пациенты старше 30 лет (filter):")
    adults = coll.filter(lambda p: p.age > 30)
    for patient in adults:
        print(f"   - {patient.display()}")
    
    # 4. map() - извлечение ФИО (изменение типа: Patient → str)
    print("\n map() -> извлечение ФИО (Patient → str):")
    names: list[str] = coll.map(lambda p: p.fio)
    print(f"   {names}")
    
    # 5. map() - извлечение стоимости лечения (Patient → float)
    print("\n map() -> стоимость лечения (Patient → float):")
    costs: list[float] = coll.map(lambda p: p.calculate_treatment_cost())
    print(f"   {[f'{c:.0f}' for c in costs]}")
    
    # 6. map() - извлечение возраста (Patient → int)
    print("\n map() -> возраст (Patient → int):")
    ages: list[int] = coll.map(lambda p: p.age)
    print(f"   {ages}")
    
    # 7. Демонстрация смены типа (главное для 4-й оценки)
    print("\n Демонстрация смены типа результата (метод map):")
    result1 = coll.map(lambda p: p.fio)           # Тип: list[str]
    result2 = coll.map(lambda p: p.age)           # Тип: list[int]
    result3 = coll.map(lambda p: p.calculate_treatment_cost())  # Тип: list[float]
    print(f"   Patient → str:  {result1[:3]}...")
    print(f"   Patient → int:  {result2[:3]}...")
    print(f"   Patient → float: {result3[:3]}...")


def demo_level5() -> None:
    # Оценка 5: демонстрация Protocol и TypeVar с bound.
    print("==== Protocol (структурная типизация) ==== ")
    
    patients = create_patients()
    
    # Сценарий 1: Displayable коллекция
    print("\n📌 Сценарий 1: TypedCollection[Displayable]")
    displayable_coll = TypedCollection[Displayable]()
    
    for p in patients:
        displayable_coll.add(p)
    
    print("   Displayable объекты в коллекции:")
    for item in displayable_coll.get_all():
        print(f"      - {item.display()}")
    
    # Сценарий 2: Scorable коллекция
    print("\n📌 Сценарий 2: TypedCollection[Scorable]")
    scorable_coll = TypedCollection[Scorable]()
    
    for p in patients:
        scorable_coll.add(p)
    
    print("   Scorable объекты и их score (стоимость лечения):")
    for item in scorable_coll.get_all():
        print(f"      - {item.display()} → score: {item.score():.0f} руб.")
    
    # Анализ через map + sum (простой способ)
    print("\n Анализ через map + sum:")
    scores = scorable_coll.map(lambda p: p.score())
    total_score = sum(scores)
    print(f"   Общая стоимость лечения всех пациентов: {total_score:.0f} руб.")
    
    # Анализ через reduce (демонстрация правильного использования) 
    print("\n Анализ через reduce (аккумулятор отдельно):")
    total_score_reduce = scorable_coll.reduce(lambda acc, p: acc + p.score(), 0.0)
    print(f"   Общая стоимость через reduce: {total_score_reduce:.0f} руб.")
    
    #  Демонстрация: классы НЕ наследуются от Protocol 
    print("\n Проверка: классы Patient, InpatientPatient, OutpatientPatient")
    print("   НЕ наследуются от Displayable или Scorable, но подходят под протоколы,")
    print("   так как имеют методы display() и score() — это структурная типизация!")
    
    test_patient = patients[0]
    print(f"\n   isinstance(Patient, Displayable) = {isinstance(test_patient, Displayable)}")
    print(f"   (но пациент всё равно подходит под протокол, потому что у него есть display())")

def main() -> None:
    print("\n" + " ЛАБОРАТОРНАЯ РАБОТА №6 (Generics и Typing) ")
    
    demo_level3()
    demo_level4()
    demo_level5()
    

if __name__ == "__main__":
    main()