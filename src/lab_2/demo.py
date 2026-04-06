from models import Patient
from collection import PatientList

def print_separator(title):
    print('='*60)
    print(f"  {title}")


def print_patients(collection, title="Список пациентов"):
    print(f"\n{title} (всего: {len(collection)}):")
    for patient in collection:
        print(f"  • {patient}")


# СЦЕНАРИЙ 1: Базовые операции
print_separator("СЦЕНАРИЙ 1: Базовые операции (добавление, удаление, итерация, len)")
p1 = Patient("Иванов Иван Петрович", 35, "Гипертония", "001")
p2 = Patient("Петрова Мария Сергеевна", 28, "Гастрит", "002")
p3 = Patient("Сидоров Алексей Владимирович", 45, "Диабет", "003")
p4 = Patient("Козлова Екатерина Андреевна", 22, "Ангина", "004")

clinic = PatientList()
clinic.add(p1)
clinic.add(p2)
clinic.add(p3)
clinic.add(p4)

print_patients(clinic, "После добавления пациентов")

print(f"\nКоличество пациентов через len(): {len(clinic)}")

print("\nИтерация через for:")
for i, patient in enumerate(clinic, 1):
    print(f"  {i}. {patient.fio} - {patient.diagnosis}")

clinic.remove(p2)
print_patients(clinic, "После удаления Петровой М.С.")

clinic.remove_at(0) 
print_patients(clinic, "После удаления по индексу 0")


#СЦЕНАРИЙ 2: Поиск и сортировка
print_separator("СЦЕНАРИЙ 2: Поиск и сортировка")

clinic.add(p1)
clinic.add(p2)
print_patients(clinic, "Восстановили всех пациентов")

print("\n Поиск по ФИО")
found = clinic.find_by_fio("Иванов")
for p in found:
    print(f"  Найден: {p}")

print("\n Поиск по диагнозу")
found = clinic.find_by_diagnosis("гастрит")
for p in found:
    print(f"  Найден: {p}")

print("\n Поиск по номеру карты")
found = clinic.find_by_id("003")
print(f"  Найден: {found}")

print("\n Сортировка по ФИО (А-Я)")
clinic.sort_by_fio()
print_patients(clinic, "Отсортировано по ФИО")

print("\n Сортировка по возрасту (от младших к старшим)")
clinic.sort_by_age()
print_patients(clinic, "Отсортировано по возрасту")


print("\n Сортировка по номеру карты")
clinic.sort_by_record_number()
print_patients(clinic, "Отсортировано по номеру карты")


# СЦЕНАРИЙ 3: Фильтрация и проверка дубликатов 
print_separator("СЦЕНАРИЙ 3: Фильтрация и защита от дубликатов")

print("\n Фильтрация по статусу")
p3.discharge()

active = clinic.get_active()
print_patients(active, "Активные пациенты")

discharged = clinic.get_discharged()
print_patients(discharged, "Выписанные пациенты")

print("\n Фильтрация по возрасту")
adults = clinic.get_adults()
print_patients(adults, "Совершеннолетние пациенты (18+)")

young = clinic.get_by_min_age(30)
print_patients(young, "Пациенты старше 30 лет")

print("\n Проверка защиты от дубликатов")
try:
    clinic.add(p1)  # p1 уже есть
    print("  ОШИБКА: дубликат добавился!")
except ValueError as e:
    print(f"  Ожидаемая ошибка: {e}")

print("\n Проверка типа добавляемого объекта")
try:
    clinic.add("Это строка, а не пациент")
    print("  ОШИБКА: строка добавилась")
except TypeError as e:
    print(f" Ожидаемая ошибка: {e}")

# Проверка индексации
print("\n--- Проверка индексации ---")
print(f"  Первый пациент: {clinic[0].fio}")
print(f"  Второй пациент: {clinic[1].fio}")
print(f"  Последний пациент: {clinic[-1].fio}")


#ИТОГОВЫЙ ВЫВОД
print_separator("ИТОГОВОЕ СОСТОЯНИЕ КОЛЛЕКЦИИ")
print_patients(clinic, "Все пациенты в коллекции")
print(f"\nПроверка методов:")
print(f"  len(clinic) = {len(clinic)}")
print(f"  clinic[0] = {clinic[0].fio}")
print(f"  Работает итерация: {', '.join([p.fio.split()[0] for p in clinic])}")