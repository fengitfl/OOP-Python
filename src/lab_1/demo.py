from models import Patient

if __name__ == "__main__":
    print("=== Демонстрация работы класса Patient ===\n")

    # 1. Создание объектов
    p1 = Patient("Иван Петров", 35, "Гипертония", "A123")
    p2 = Patient("Мария Смирнова", 28, "Грипп", "B456")
    p3 = Patient("Иван Петров", 35, "Гипертония", "A123") 
    # 2. Вывод через print (используется __str__)
    print("Объект p1:")
    print(p1)
    print("\nОбъект p2:")
    print(p2)
    print("Объект p3:")
    print(p3)

    # 3. Сравнение (__eq__)
    print("\nСравнение p1 и p2 по номеру карты:", p1 == p2)
    print("Сравнение p1 и p3 (одинаковый номер):", p1 == p3)

    # 4. Некорректное создание (try/except)
    print("\nПопытка создать пациента с недопустимым возрастом:")
    try:
        p_bad = Patient("Олег", -5, "Ангина", "C789")
    except ValueError as e:
        print("Ошибка:", e)

    # 5. Изменение свойства через сеттер (с валидацией)
    print("\nИзменение возраста p1:")
    p1.age = 36
    print(f"Новый возраст: {p1.age}")
    try:
        p1.age = 150
    except ValueError as e:
        print("Ошибка при попытке установить 150 лет:", e)

    # 6. Доступ к атрибуту класса
    print("\nАтрибут класса total_patients:")
    print("Через класс:", Patient.total_patients)
    print("Через экземпляр p1:", p1.total_patients)

    # 7. Бизнес-методы и состояния
    print("\nПроверка can_prescribe_medicine для p1 (активен, возраст 36):", p1.can_prescribe_medicine())
    print("Выписываем p1...")
    p1.discharge()
    print(p1)  # статус изменился
    print("can_prescribe_medicine после выписки:", p1.can_prescribe_medicine())

    try:
        p1.update_diagnosis("Новый диагноз")
    except RuntimeError as e:
        print("Ошибка при смене диагноза выписанному пациенту:", e)

    # 8. Демонстрация __repr__
    print("\nrepr(p1):", repr(p1))

    # 9. Дополнительно: создание ещё одного пациента для проверки счётчика
    p4 = Patient("Елена", 45, "Артрит", "D999")
    print(f"\nСоздан ещё один пациент. Теперь всего пациентов: {Patient.total_patients}")