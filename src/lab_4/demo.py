from datetime import date
from models import Patient, InpatientPatient, OutpatientPatient
from interfaces import Treatable, Diagnosable, Comparable

def print_treatment_costs(items: list[Treatable]):
    print("\n=== Стоимость лечения (интерфейс Treatable) ===")
    for obj in items:
        cost = obj.calculate_cost()
        if isinstance(obj, Diagnosable):
            info = obj.get_diagnosis_info()
        else:
            info = str(obj)
        print(f"{info[:55]:<55} | Стоимость: {cost} руб.")

def sort_by_age(items: list):
    return sorted(items, key=lambda p: p.age)

def demo():
    # 1. СОЗДАНИЕ ОБЪЕКТОВ С ДАННЫМИ
    print("=== СОЗДАНИЕ ОБЪЕКТОВ ===")
    
    p1 = Patient("Иванов Иван", 45, "Гипертония", "001")
    print(f"Создан: {p1.fio}")
    
    p2 = InpatientPatient("Петрова Анна", 68, "Пневмония", "002", 
                          ward=302, daily_rate=5500)
    p2.add_days(7)  # добавляем 7 дней
    print(f"Создан: {p2.fio}, добавлено дней: {p2.days_stayed}")
    
    p3 = OutpatientPatient("Сидоров Олег", 20, "Мигрень", "003",
                           next_appointment=date(2026,5,15),
                           attending_doctor="Доктор Хаус",
                           consultation_price=2500)
    p3.add_visit()  # обавляем визиты
    p3.add_visit()
    p3.add_visit()  # 3 визита
    print(f"Создан: {p3.fio}, визитов: {p3.visits_count}")

    patients = [p1, p2, p3]

    # 2. ДЕМОНСТРАЦИЯ ИНТЕРФЕЙСА DIAGNOSABLE
    print("\n=== Демонстрация интерфейса Diagnosable ===")
    for p in patients:
        if isinstance(p, Diagnosable):
            print(p.get_diagnosis_info())

    # 3. ДЕМОНСТРАЦИЯ ИНТЕРФЕЙСА TREATABLE 
    print_treatment_costs(patients)

    print("\n=== Проверка реализации интерфейсов (isinstance) ===")
    for p in patients:
        print(f"{p.fio}: Treatable? {isinstance(p, Treatable)}, "
              f"Diagnosable? {isinstance(p, Diagnosable)}, "
              f"Comparable? {isinstance(p, Comparable)}")

    # 5. ФИЛЬТРАЦИЯ ПО ИНТЕРФЕЙСУ
    treatable_objects = [p for p in patients if isinstance(p, Treatable)]
    print(f"\nОбъектов, реализующих Treatable: {len(treatable_objects)}")

    # 6. СОРТИРОВКА ПО ВОЗРАСТУ
    p4 = Patient("Алексеев Дмитрий", 30, "Здоров", "004")
    p5 = InpatientPatient("Морозова Елена", 55, "Гастрит", "005", ward=101, daily_rate=4000)
    p5.add_days(3)  # Добавляем дни и для этого пациента
    unsorted = [p4, p2, p5, p1, p3]
    sorted_by_age = sort_by_age(unsorted)
    
    print("\n=== Сортировка по возрасту (используя поле age) ===")
    for p in sorted_by_age:
        print(f"{p.fio}: {p.age} лет")

    # 7. ПОЛИМОРФИЗМ БЕЗ УСЛОВИЙ
    def process_treatment(obj: Treatable):
        return f"Сумма к оплате: {obj.calculate_cost():.2f} руб."

    print("\n=== Полиморфизм без условий ===")
    for p in patients:
        print(process_treatment(p))
    
    # 8. ДОПОЛНИТЕЛЬНО: ПОКАЗЫВАЕМ ФОРМУЛЫ РАСЧЁТА
    print("\n=== ПОЯСНЕНИЕ РАСЧЁТОВ ===")
    print(f"Петрова Анна: {p2.daily_rate} руб/день × {p2.days_stayed} дней = {p2.calculate_cost()} руб.")
    print(f"Сидоров Олег: {p3.consultation_price} руб/визит × {p3.visits_count} визитов = {p3.calculate_cost()} руб.")

if __name__ == "__main__":
    demo()