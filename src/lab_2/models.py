class Patient:

    total_patients = 0

    def __init__(self, fio, age, diagnosis, record_number):

        self.__fio = None
        self.__age = None
        self.__diagnosis = None
        self.__record_number = None
        self.__is_active = True  
        self.fio =fio
        self.age = age
        self.diagnosis = diagnosis
        self.record_number = record_number

        Patient.total_patients += 1

    @property
    def fio(self):
        return self.__fio

    @fio.setter
    def fio(self, value):
        validate_fio(value)
        self.__fio = value.strip()

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
        self.__diagnosis = value.strip() if value else ""  

    @property
    def record_number(self):
        return self.__record_number

    @record_number.setter
    def record_number(self, value):
        validate_record_number(value)
        self.__record_number = str(value).strip() 

    @property
    def is_active(self):
        return self.__is_active

    def discharge(self):
        if not self.__is_active:
            raise RuntimeError("Пациент уже выписан")
        self.__is_active = False

    def reinstate(self):
        if self.__is_active:
            raise RuntimeError("Пациент уже активен")
        self.__is_active = True

    def update_diagnosis(self, new_diagnosis):
        if not self.__is_active:
            raise RuntimeError("Нельзя изменить диагноз выписанного пациента")
        validate_diagnosis(new_diagnosis)
        self.__diagnosis = new_diagnosis.strip() if new_diagnosis else ""

    def can_prescribe_medicine(self):
        return self.__is_active and self.__age >= 18

    def __str__(self):
        status = "активен" if self.__is_active else "выписан"
        return (f"Пациент: {self.__fio}, возраст: {self.__age}, "
                f"диагноз: '{self.__diagnosis}', номер карты: {self.__record_number}, "
                f"статус: {status}")

    def __repr__(self):
        return (f"Patient(fio={self.__fio!r}, age={self.__age}, "
                f"diagnosis={self.__diagnosis!r}, record_number={self.__record_number!r})")

    def __eq__(self, other):
        if not isinstance(other, Patient):
            return False
        return self.__record_number == other.__record_number
def validate_fio(value: str):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("ФИО должно быть непустой строкой")

def validate_age(value: int):
    if type(value) is not int:
        raise TypeError("Возраст должен быть целым числом")
    if value < 0 or value > 120:
        raise ValueError("Возраст должен быть в диапазоне 0–120")

def validate_diagnosis(value: str):
    if not isinstance(value, str):
        raise TypeError("Диагноз должен быть строкой")

def validate_record_number(value):
    if not isinstance(value, (str, int)):
        raise TypeError("Номер карты должен быть строкой или числом")
    if str(value).strip() == "":
        raise ValueError("Номер карты не может быть пустым")