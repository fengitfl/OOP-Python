from validate import validate_name, validate_age, validate_diagnosis, validate_record_number

class Patient:

    # Атрибут класса: общее количество созданных пациентов
    total_patients = 0

    def __init__(self, name, age, diagnosis, record_number):
        # Сначала инициализируем закрытые поля значением None
        # Это позволяет избежать ошибок при вызове сеттеров
        self.__name = None
        self.__age = None
        self.__diagnosis = None
        self.__record_number = None
        self.__is_active = True  # состояние: активен / выписан

        # Используем сеттеры для присваивания значений с проверкой
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.record_number = record_number

        # Увеличиваем счётчик пациентов
        Patient.total_patients += 1

    # Свойства (геттеры и сеттеры)
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        validate_name(value)
        self.__name = value.strip()

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        validate_age(value)
        self.__age = value

    @property
    def diagnosis(self):
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, value):
        validate_diagnosis(value)
        self.__diagnosis = value.strip() if value else ""  # сохраняем как есть

    @property
    def record_number(self):
        return self.__record_number

    @record_number.setter
    def record_number(self, value):
        validate_record_number(value)
        self.__record_number = str(value).strip()  # храним как строку

    @property
    def is_active(self):
        return self.__is_active
    # сеттер для is_active не делаем — состояние меняется через бизнес-методы

    # Методы изменения состояния 
    def discharge(self):
        # Выписать пациента (деактивировать)
        if not self.__is_active:
            raise RuntimeError("Пациент уже выписан")
        self.__is_active = False

    def reinstate(self):
        # Восстановить пациента (если был выписан)
        if self.__is_active:
            raise RuntimeError("Пациент уже активен")
        self.__is_active = True

    def update_diagnosis(self, new_diagnosis):
        # Изменить диагноз (только для активного пациента)
        if not self.__is_active:
            raise RuntimeError("Нельзя изменить диагноз выписанного пациента")
        validate_diagnosis(new_diagnosis)
        self.__diagnosis = new_diagnosis.strip() if new_diagnosis else ""

    def can_prescribe_medicine(self):
        # Проверка, может ли пациент получать лекарства (активен и возраст ≥ 18)
        return self.__is_active and self.__age >= 18

    # Магические метод
    def __str__(self):
        # Читаемое представление для пользователя.
        status = "активен" if self.__is_active else "выписан"
        return (f"Пациент: {self.__name}, возраст: {self.__age}, "
                f"диагноз: '{self.__diagnosis}', номер карты: {self.__record_number}, "
                f"статус: {status}")

    def __repr__(self):
        # Официальное представление для отладки
        return (f"Patient(name={self.__name!r}, age={self.__age}, "
                f"diagnosis={self.__diagnosis!r}, record_number={self.__record_number!r})")

    def __eq__(self, other):
        # Сравнение пациентов по уникальному номеру карты
        if not isinstance(other, Patient):
            return False
        return self.__record_number == other.__record_number