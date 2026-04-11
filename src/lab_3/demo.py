from datetime import date
from base import Patient
from models import InpatientPatient, OutpatientPatient

def demonstrate_lab3():

    print("ЛАБОРАТОРНАЯ РАБОТА №3: Наследование и полиморфизм")
    
    # СЦЕНАРИЙ 1: Создание объектов разных типов
    print("\n1. СОЗДАНИЕ ОБЪЕКТОВ РАЗНЫХ ТИПОВ")
    print("-" * 40)
    
    # Обычный пациент (базовый класс)
    patient1 = Patient("Иванов Иван Иванович", 45, "Гипертония", "12345")
    
    # Стационарный пациент
    inpatient = InpatientPatient(
        fio="Петрова Анна Сергеевна",
        age=68,
        diagnosis="Пневмония",
        record_number="67890",
        ward=302,
        admission_date=date(2026, 4, 1),
        daily_rate=5500
    )
    
    # Амбулаторный пациент
    outpatient = OutpatientPatient(
        fio="Сидоров Олег Викторович",
        age=20,
        diagnosis="Мигрень",
        record_number="11223",
        next_appointment=date(2026, 5, 15),
        attending_doctor="Доктор Хаус Г.Г.",
        insurance_company="СОГАЗ",
        consultation_price=2500
    )
    
    print(f" Создан: {patient1}")
    print(f" Создан: {inpatient}")
    print(f" Создан: {outpatient}")
    
    # СЦЕНАРИЙ 2: Полиморфное поведение 
    print("\n2. ПОЛИМОРФНОЕ ПОВЕДЕНИЕ (один метод - разная реализация)")
    print("-" * 40)
    
    # Добавляем дни лечения и визиты
    inpatient.add_days(7)
    outpatient.add_visit()
    outpatient.add_visit()
    outpatient.add_visit()
    
    patients = [patient1, inpatient, outpatient]
    
    for patient in patients:
        try:
            cost = patient.calculate_treatment_cost()
            patient_type = patient.get_patient_type()
            print(f"{patient_type} {patient.fio}:")
            print(f"  Стоимость лечения: {cost} руб.")
            print(f"  Статус: {'Активен' if patient.is_active else 'Выписан'}")
        except Exception as e:
            print(f"  Ошибка: {e}")
    
    #СЦЕНАРИЙ 3: Использование методов дочерних классов
    print("\n3. МЕТОДЫ ДОЧЕРНИХ КЛАССОВ")
    print("-" * 40)
    
    # Методы InpatientPatient
    print(inpatient.change_ward(305))
    inpatient.add_days(3)
    print(f"После добавления дней: {inpatient.days_stayed} дней в стационаре")
    
    # Методы OutpatientPatient
    print(outpatient.add_visit())
    print(outpatient.reschedule_appointment(date(2026, 5, 20)))
    
    # СЦЕНАРИЙ 4: Проверка типов через isinstance() 
    print("\n4. ПРОВЕРКА ТИПОВ (isinstance)")
    print("-" * 40)
    
    print(f"inpatient - Patient? {isinstance(inpatient, Patient)}")
    print(f"inpatient - InpatientPatient? {isinstance(inpatient, InpatientPatient)}")
    print(f"inpatient - OutpatientPatient? {isinstance(inpatient, OutpatientPatient)}")
    
    print(f"outpatient - Patient? {isinstance(outpatient, Patient)}")
    print(f"outpatient - OutpatientPatient? {isinstance(outpatient, OutpatientPatient)}")
    
    # СЦЕНАРИЙ 5: Фильтрация коллекции по типу
    print("\n5. ФИЛЬТРАЦИЯ КОЛЛЕКЦИИ ПО ТИПУ")
    print("-" * 40)
    
    all_patients = [
        Patient("Тестов1", 30, "Диагноз1", "001"),
        InpatientPatient("Тестов2", 40, "Диагноз2", "002", ward=101),
        OutpatientPatient("Тестов3", 50, "Диагноз3", "003"),
        InpatientPatient("Тестов4", 60, "Диагноз4", "004", ward=102),
        OutpatientPatient("Тестов5", 25, "Диагноз5", "005")
    ]
    
    # Фильтрация стационарных пациентов
    inpatients = [p for p in all_patients if isinstance(p, InpatientPatient)]
    print(f"Стационарных пациентов: {len(inpatients)}")
    
    # Фильтрация амбулаторных пациентов
    outpatients = [p for p in all_patients if isinstance(p, OutpatientPatient)]
    print(f"Амбулаторных пациентов: {len(outpatients)}")
    
    # Фильтрация активных пациентов
    active_patients = [p for p in all_patients if p.is_active]
    print(f"Активных пациентов: {len(active_patients)}")
    
    #СЦЕНАРИЙ 6: Работа с коллекцией и полиморфизмом
    print("\n6. КОЛЛЕКЦИЯ + ПОЛИМОРФИЗМ")
    print("-" * 40)
    
    # Добавляем данные для расчета стоимости
    for p in all_patients:
        if isinstance(p, InpatientPatient):
            p.add_days(5)
        elif isinstance(p, OutpatientPatient):
            p.add_visit()
            p.add_visit()
    
    # Единый вызов метода для всех
    print("Стоимость лечения всех пациентов:")
    for i, patient in enumerate(all_patients, 1):
        try:
            cost = patient.calculate_treatment_cost()
            print(f"{i}. {patient.get_patient_type()} {patient.fio}: {cost} руб.")
        except:
            print(f"{i}. {patient.fio}: не может быть рассчитана")
    
    #СЦЕНАРИЙ 7: Демонстрация выписки 
    print("\n7. ВЫПИСКА ПАЦИЕНТОВ")
    print("-" * 40)
    
    inpatient.discharge()
    print(f"После выписки: {inpatient}")
    
    try:
        inpatient.change_ward(400)  # Должно вызвать ошибку
    except RuntimeError as e:
        print(f"Ошибка при попытке перевода: {e}")
    

if __name__ == "__main__":
    demonstrate_lab3()