from models import Patient, InpatientPatient, OutpatientPatient, PatientList
from interfaces import Printable, Comparable, CostCalculable
from datetime import date, timedelta

def print_all(items: list[Printable]) -> None:
    print("=== ВЫВОД через интерфейс PRINTABLE ===")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.to_string()}")


def calculate_total_cost(items: list[CostCalculable]) -> float:
    total = sum(item.calculate_cost() for item in items)
    return total

def compare_patients(patient1: Comparable, patient2: Comparable) -> str:
    result = patient1.compare_to(patient2)
    if result < 0:
        return f"{patient1.fio} < {patient2.fio}"
    elif result > 0:
        return f"{patient1.fio} > {patient2.fio}"
    else:
        return f"{patient1.fio} == {patient2.fio}"


def main():

    print("=== СЦЕНАРИЙ 1: СОЗДАНИЕ ПАЦИЕНТОВ РАЗНЫХ ТИПОВ ===")


    patient1 = Patient("Иванов Иван Иванович", 45, "Гипертония", "P001")

    inpatient = InpatientPatient(
        "Петрова Мария Сергеевна", 32, "Аппендицит", "P002",
        ward=101, daily_rate=4500
    )
    inpatient.add_days(5) 

    outpatient = OutpatientPatient(
        "Сидоров Алексей Владимирович", 28, "Грипп", "P003",
        next_appointment=date.today() + timedelta(days=7),
        attending_doctor="Смирнова Е.А.",
        insurance_company="СОГАЗ"
    )
    outpatient.add_visit()
    outpatient.add_visit()
    outpatient.add_visit()

    inpatient2 = InpatientPatient(
        "Козлов Дмитрий Петрович", 67, "Пневмония", "P004",
        ward=205, daily_rate=6000
    )
    inpatient2.add_days(10)

    print("\nСозданы объекты:")
    print(f"  - {patient1}")
    print(f"  - {inpatient}")
    print(f"  - {outpatient}")

    print("=== СЦЕНАРИЙ 2: ИСПОЛЬЗОВАНИЕ ИНТЕРФЕЙСА PRINTABLE ===" )

    printable_objects: list[Printable] = [patient1, inpatient, outpatient, inpatient2]
    
    print_all(printable_objects)

    print("\nПроверка через isinstance():")
    print(f"  patient1 implements Printable: {isinstance(patient1, Printable)}")
    print(f"  inpatient implements Printable: {isinstance(inpatient, Printable)}")
    print(f"  outpatient implements Printable: {isinstance(outpatient, Printable)}")

    print("=== СЦЕНАРИЙ 3: ИСПОЛЬЗОВАНИЕ ИНТЕРФЕЙСА COMPARABLE ===")

    print("\nСравнение пациентов (по номеру карты):")
    print(f"  {compare_patients(inpatient, inpatient2)}")
    
    print("\nДо сортировки по номеру карты:")
    collection = PatientList()
    collection.add(inpatient2)  # P004
    collection.add(patient1)    # P001
    collection.add(inpatient)   # P002
    collection.add(outpatient)  # P003
    
    for p in collection:
        print(f"    {p.fio}: карта №{p.record_number}")

    print("\nПосле сортировки через интерфейс Comparable:")
    collection.sort_by_comparable()
    for p in collection:
        print(f"    {p.fio}: карта №{p.record_number}")

    print("=== СЦЕНАРИЙ 4: ИСПОЛЬЗОВАНИЕ ИНТЕРФЕЙСА COSTCALCULABLE ===")

    calculable_objects: list[CostCalculable] = [inpatient, outpatient, inpatient2]

    print("\nИнформация о стоимости лечения:")
    for obj in calculable_objects:
        print(f"  {obj.fio}: {obj.calculate_cost():.2f} руб.")
        print(f"    Детали: {obj.get_diagnosis_info()}")

    total = calculate_total_cost(calculable_objects)
    print(f"\nОбщая стоимость лечения всех пациентов: {total:.2f} руб.")

    print("=== СЦЕНАРИЙ 5: ПРОВЕРКА МНОЖЕСТВЕННОЙ РЕАЛИЗАЦИИ ИНТЕРФЕЙСОВ ===")

    test_patient = OutpatientPatient(
        "Тестов Тест Тестович", 35, "Здоров", "P999",
        attending_doctor="Доктор Айболит"
    )

    print(f"\nОбъект {test_patient.fio} реализует интерфейсы:")
    print(f"Printable:     {isinstance(test_patient, Printable)}")
    print(f"Comparable:    {isinstance(test_patient, Comparable)}")
    print(f"CostCalculable:{isinstance(test_patient, CostCalculable)}")
    print(f"Diagnosable:   {isinstance(test_patient, Diagnosable)}")
    print(f"Treatable:     {isinstance(test_patient, Treatable)}")

    print("=== СЦЕНАРИЙ 6: ФИЛЬТРАЦИЯ КОЛЛЕКЦИИ ПО ИНТЕРФЕЙСАМ ===")

    large_collection = PatientList()
    large_collection.add(patient1)
    large_collection.add(inpatient)
    large_collection.add(inpatient2)
    large_collection.add(outpatient)

    print(f"\nВсего пациентов в коллекции: {len(large_collection)}")
    
    # Фильтрация по интерфейсам
    printable_patients = large_collection.get_printable()
    calculable_patients = large_collection.get_cost_calculable()
    
    print(f"\nПациенты, реализующие Printable: {len(printable_patients)}")
    print(f"Пациенты, реализующие CostCalculable: {len(calculable_patients)}")
    
    print("\nИнформация о пациентах с CostCalculable:")
    for p in calculable_patients:
        print(f"  • {p.fio}: стоимость лечения = {p.calculate_cost():.2f} руб.")

if __name__ == "__main__":
    from interfaces import Diagnosable, Treatable
    main()