from abc import ABC, abstractmethod
from datetime import date

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

class Treatable(ABC):

    @abstractmethod
    def calculate_cost(self):
        pass

class Diagnosable(ABC):

    @abstractmethod
    def get_diagnosis_info(self):
        pass

class Comparable(ABC):

    @abstractmethod
    def compare_to(self, other):
        pass
    
class Patient(Treatable, Diagnosable):
    total_patients = 0

    def __init__(self, fio, age, diagnosis, record_number):
        self.__fio = None
        self.__age = None
        self.__diagnosis = None
        self.__record_number = None
        self.__is_active = True  
        self.fio = fio
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
    
    # Реализация интерфейсов
    def calculate_cost(self) -> float:
        return 0.0

    def get_diagnosis_info(self) -> str:
        return f"Диагноз: {self.diagnosis}. Пациент: {self.fio}"

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


class InpatientPatient(Patient):
    def __init__(self, fio, age, diagnosis, record_number, ward, admission_date=None, daily_rate=5000):
        super().__init__(fio, age, diagnosis, record_number)
        self._ward = None
        self.ward = ward
        self.admission_date = admission_date if admission_date else date.today()
        self.daily_rate = daily_rate
        self._days_stayed = 0  # Используем защищённый атрибут

    @property
    def ward(self):
        return self._ward

    @ward.setter
    def ward(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номер палаты должен быть положительным целым числом")
        self._ward = value

    @property
    def days_stayed(self):
        return self._days_stayed

    def change_ward(self, new_ward):
        if not self.is_active:
            raise RuntimeError("Нельзя перевести выписанного пациента")
        old_ward = self._ward
        self.ward = new_ward
        return f"Пациент переведён из палаты {old_ward} в палату {new_ward}"

    def add_days(self, days):
        if days <= 0:
            raise ValueError("Количество дней должно быть положительным")
        self._days_stayed += days

    def calculate_cost(self) -> float:
        return self.daily_rate * self._days_stayed

    def get_diagnosis_info(self) -> str:
        return (f"Стационарный пациент {self.fio}, диагноз: {self.diagnosis}. "
                f"Требуется госпитализация, палата {self.ward}")

    def __str__(self):
        base_str = super().__str__()
        return (f"{base_str}, палата: {self._ward}, "
                f"дней в стационаре: {self._days_stayed}, "
                f"поступление: {self.admission_date.isoformat()}")

    def __repr__(self):
        return (f"InpatientPatient(fio={self.fio!r}, age={self.age}, "
                f"diagnosis={self.diagnosis!r}, record_number={self.record_number!r}, "
                f"ward={self.ward}, admission_date={self.admission_date.isoformat()!r})")


class OutpatientPatient(Patient):
    def __init__(self, fio, age, diagnosis, record_number, next_appointment=None,
                 attending_doctor=None, insurance_company=None, consultation_price=2000):
        
        super().__init__(fio, age, diagnosis, record_number)
        self._next_appointment = None
        self._attending_doctor = None
        self._insurance_company = None
        self.next_appointment = next_appointment
        self.attending_doctor = attending_doctor
        self.insurance_company = insurance_company
        self.consultation_price = consultation_price
        self._visits_count = 0  # Используем защищённый атрибут

    @property
    def next_appointment(self):
        return self._next_appointment

    @next_appointment.setter
    def next_appointment(self, value):
        if value is not None and not isinstance(value, date):
            raise TypeError("Дата визита должна быть объектом date или None")
        if value is not None and value < date.today():
            raise ValueError("Дата следующего визита не может быть в прошлом")
        self._next_appointment = value

    @property
    def attending_doctor(self):
        return self._attending_doctor

    @attending_doctor.setter
    def attending_doctor(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("ФИО врача должно быть строкой")
            if not value.strip():
                raise ValueError("ФИО врача не может быть пустым")
            value = value.strip()
        self._attending_doctor = value

    @property
    def insurance_company(self):
        return self._insurance_company

    @insurance_company.setter
    def insurance_company(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("Страховая компания должна быть строкой")
            if not value.strip():
                raise ValueError("Страховая компания не может быть пустой строкой")
            value = value.strip()
        self._insurance_company = value

    @property
    def visits_count(self):
        return self._visits_count

    def add_visit(self):
        if not self.is_active:
            raise RuntimeError("Выписанный пациент не может посещать врача")
        self._visits_count += 1
        return f"Визит #{self._visits_count} зарегистрирован"

    def reschedule_appointment(self, new_date):
        if new_date < date.today():
            raise ValueError("Новая дата не может быть в прошлом")
        old_date = self._next_appointment
        self.next_appointment = new_date
        return f"Визит перенесён с {old_date} на {new_date}"

    # ПЕРЕОПРЕДЕЛЯЕМ МЕТОД calculate_cost
    def calculate_cost(self) -> float:
        return self.consultation_price * self._visits_count

    def get_diagnosis_info(self) -> str:
        next_date = self._next_appointment.isoformat() if self._next_appointment else "не назначен"
        doctor = self._attending_doctor if self._attending_doctor else "не назначен"
        return (f"Амбулаторный пациент {self.fio}, диагноз: {self.diagnosis}. "
                f"Следующий визит: {next_date}, врач: {doctor}")

    def can_prescribe_medicine(self):
        if self.age < 21:
            return False
        return super().can_prescribe_medicine()

    def __str__(self):
        base_str = super().__str__()
        next_date = self._next_appointment.isoformat() if self._next_appointment else "не назначен"
        doctor = self._attending_doctor if self._attending_doctor else "не назначен"
        insurance = self._insurance_company if self._insurance_company else "не указана"
        return (f"{base_str}, следующий визит: {next_date}, "
                f"врач: {doctor}, страховка: {insurance}, "
                f"визитов: {self._visits_count}")

    def __repr__(self):
        next_date = self._next_appointment.isoformat() if self._next_appointment else None
        return (f"OutpatientPatient(fio={self.__fio!r}, age={self.__age}, "
                f"diagnosis={self.__diagnosis!r}, record_number={self.__record_number!r}, "
                f"next_appointment={next_date!r}, "
                f"attending_doctor={self._attending_doctor!r}, "
                f"insurance_company={self._insurance_company!r})")
