class Patient:

    total_patients = 0 
    
    def __init__(self, name, age, diagnosis, record_number):

        self._validate_name(name)
        self._validate_age(age)
        self._validate_diagnosis(diagnosis)
        self._validate_record_number(record_number)

        self._name = name
        self._age = age
        self._diagnosis = diagnosis
        self._record_number = record_number
        self._is_active = True
        Patient.total_patients += 1

    def _validate_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя должно быть непустой строкой")
        
    def _validate_age(self, age):
        if not type(age) is int:
            raise TypeError("Возраст должно быть целым числом")
        if 0 > age < 130:
            raise ValueError("Возраст должен быть в пределе от 0 до 130")
    
    def _validate_diagnosis(self, diagnosis):
        if not isinstance(diagnosis, str):
            raise TypeError("Диагноз должен быть строкой")

    def _validate_record_number(self, record_number):
        if not isinstance(record_number, (str, int)):
            raise TypeError("Номер карты должен быть строкой или числом")
        if str(record_number).strip() == "":
            raise ValueError("Номер карты не может быть пустым")    
    
    # -------- Свойства ( геттеры) -------

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._validate_name(new_name)
        self._name = new_name
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, new_age):
        self._validate_age(new_age)
        self._age = new_age

    @property
    def diagnosis(self):
        return self._diagnosis

    @diagnosis.setter
    def diagnosis(self, new_diagnosis):
        self._validate_diagnosis(new_diagnosis)
        self._diagnosis = new_diagnosis

    @property
    def record_number(self):
        return self._record_number

    @property
    def is_active(self):
        return self._is_active
    
    # ---------- Магические методы ----------
    def __str__(self):
        status = "активен" if self._is_active else "выписан"
        return f"Пациент: {self._name}, {self._age} лет, диагноз: '{self._diagnosis}', статус: {status}"

    def __repr__(self):
        return (f"Patient(name={self._name!r}, age={self._age}, "
                f"diagnosis={self._diagnosis!r}, record_number={self._record_number!r})")

    def __eq__(self, other):
        """Сравнение пациентов по уникальному номеру карты."""
        if not isinstance(other, Patient):
            return False
        return self._record_number == other._record_number

    # ---------- Бизнес-методы ----------
    def discharge(self):
        """Выписать пациента (деактивировать)."""
        if not self._is_active:
            raise RuntimeError("Пациент уже выписан")
        self._is_active = False

    def update_diagnosis(self, new_diagnosis):
        """Изменить диагноз (только для активного пациента)."""
        if not self._is_active:
            raise RuntimeError("Нельзя изменить диагноз выписанного пациента")
        self._validate_diagnosis(new_diagnosis)
        self._diagnosis = new_diagnosis

    def can_prescribe_medicine(self):
        """Проверка, может ли пациент получать лекарства (активен и совершеннолетний)."""
        return self._is_active and self._age >= 18

