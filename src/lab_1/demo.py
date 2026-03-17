from models import Patient

def main():
    print("=== Демонстрация работы класса Patient ===\n")

    # 1. Создание объектов
    p1 = Patient("Иван Петров", 35, "Гипертония", "A123")
    p2 = Patient("Мария Смирнова", 28, "Грипп", "B456")

    print("Созданы пациенты:")
    print(p1)
    print(p2)

    # 2. Сравнение (__eq__)
    p3 = Patient("Иван Петров", 35, "Гипертония", "A123")  # тот же номер
    print("\nСравнение p1 и p3 (одинаковый номер карты):", p1 == p3)
    print("Сравнение p1 и p2:", p1 == p2)

    # 3. Обработка ошибок при создании
    print("\nПопытка создать пациента с недопустимым возрастом:")
    try:
        p_bad = Patient("Олег", -5, "Ангина", "C789")
    except ValueError as e:
        print("Ошибка:", e)

    print("\nПопытка создать пациента с булевым значением возраста:")
    try:
        p_bad = Patient("Олег", True, "Ангина", "C789")
    except TypeError as e:
        print("Ошибка:", e)

    # 4. Изменение свойств через сеттеры (с валидацией)
    print("\nИзменение возраста p1:")
    p1.age = 36
    print(f"Новый возраст: {p1.age}")
    try:
        p1.age = 150
    except ValueError as e:
        print("Ошибка при попытке установить 150 лет:", e)

    # 5. Доступ к атрибуту класса
    print(f"\nАтрибут класса total_patients: {Patient.total_patients}")
    print(f"Через экземпляр p1: {p1.total_patients}")

    # 6. Бизнес-методы и логика состояний
    print("\nПроверка can_prescribe_medicine для p1:", p1.can_prescribe_medicine())
    print("Выписываем p1...")
    p1.discharge()
    print(p1)
    print("can_prescribe_medicine после выписки:", p1.can_prescribe_medicine())

    try:
        p1.update_diagnosis("Новый диагноз")
    except RuntimeError as e:
        print("Ошибка при смене диагноза выписанному пациенту:", e)

    print("\nВосстанавливаем p1...")
    p1.reinstate()
    print(p1)
    p1.update_diagnosis("Хронический бронхит")
    print("После изменения диагноза:", p1)

    # 7. Демонстрация __repr__
    print("\nrepr(p1):", repr(p1))

    # 8. Создание ещё одного пациента для проверки счётчика
    p4 = Patient("Елена", 45, "Артрит", "D999")
    print(f"\nСоздан ещё один пациент. Всего пациентов: {Patient.total_patients}")

if __name__ == "__main__":
    main()