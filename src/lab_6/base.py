from datetime import date

def validate_fio(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("ФИО должно быть непустой строкой")

def validate_age(value: int) -> None:
    if type(value) is not int:
        raise TypeError("Возраст должен быть целым числом")
    if value < 0 or value > 120:
        raise ValueError("Возраст должен быть в диапазоне 0–120")

def validate_diagnosis(value: str) -> None:
    if not isinstance(value, str):
        raise TypeError("Диагноз должен быть строкой")

def validate_record_number(value: str | int) -> None:
    if not isinstance(value, (str, int)):
        raise TypeError("Номер карты должен быть строкой или числом")
    if str(value).strip() == "":
        raise ValueError("Номер карты не может быть пустым")


class Patient:
    total_patients: int = 0

    def __init__(self, fio: str, age: int, diagnosis: str, record_number: str | int) -> None:
        self.__fio: str | None = None
        self.__age: int | None = None
        self.__diagnosis: str | None = None
        self.__record_number: str | None = None
        self.__is_active: bool = True  
        self.fio = fio
        self.age = age
        self.diagnosis = diagnosis
        self.record_number = record_number
        Patient.total_patients += 1

    @property
    def fio(self) -> str:
        return self.__fio

    @fio.setter
    def fio(self, value: str) -> None:
        validate_fio(value)
        self.__fio = value.strip()

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int) -> None:
        validate_age(value)
        self.__age = value

    @property
    def diagnosis(self) -> str:
        return self.__diagnosis

    @diagnosis.setter
    def diagnosis(self, value: str) -> None:
        validate_diagnosis(value)
        self.__diagnosis = value.strip() if value else ""

    @property
    def record_number(self) -> str:
        return self.__record_number

    @record_number.setter
    def record_number(self, value: str | int) -> None:
        validate_record_number(value)
        self.__record_number = str(value).strip()

    @property
    def is_active(self) -> bool:
        return self.__is_active

    def discharge(self) -> None:
        if not self.__is_active:
            raise RuntimeError("Пациент уже выписан")
        self.__is_active = False

    def reinstate(self) -> None:
        if self.__is_active:
            raise RuntimeError("Пациент уже активен")
        self.__is_active = True

    def update_diagnosis(self, new_diagnosis: str) -> None:
        if not self.__is_active:
            raise RuntimeError("Нельзя изменить диагноз выписанного пациента")
        validate_diagnosis(new_diagnosis)
        self.__diagnosis = new_diagnosis.strip() if new_diagnosis else ""

    def can_prescribe_medicine(self) -> bool:
        return self.__is_active and self.__age >= 18

    def calculate_treatment_cost(self) -> float:
        """Стоимость лечения для обычного пациента (0 рублей)"""
        return 0.0

    def get_patient_type(self) -> str:
        """Тип пациента"""
        return "Обычный пациент"

    def display(self) -> str:
        return f"{self.get_patient_type()}: {self.fio}, {self.age} лет"

    def score(self) -> float:
        return self.calculate_treatment_cost()

    def __str__(self) -> str:
        status = "активен" if self.__is_active else "выписан"
        return (f"Пациент: {self.__fio}, возраст: {self.__age}, "
                f"диагноз: '{self.__diagnosis}', номер карты: {self.__record_number}, "
                f"статус: {status}")

    def __repr__(self) -> str:
        return (f"Patient(fio={self.__fio!r}, age={self.__age}, "
                f"diagnosis={self.__diagnosis!r}, record_number={self.__record_number!r})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Patient):
            return False
        return self.__record_number == other.__record_number


class InpatientPatient(Patient):
    def __init__(self, fio: str, age: int, diagnosis: str, record_number: str | int,
                 ward: int, admission_date: date | None = None, daily_rate: int = 5000) -> None:
        super().__init__(fio, age, diagnosis, record_number)
        self.__ward: int = ward
        self.admission_date: date = admission_date if admission_date else date.today()
        self.daily_rate: int = daily_rate
        self.days_stayed: int = 0

    @property
    def ward(self) -> int:
        return self.__ward

    @ward.setter
    def ward(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номер палаты должен быть положительным целым числом")
        self.__ward = value

    def change_ward(self, new_ward: int) -> str:
        if not self.is_active:
            raise RuntimeError("Нельзя перевести выписанного пациента")
        old_ward = self.__ward
        self.ward = new_ward
        return f"Пациент переведён из палаты {old_ward} в палату {new_ward}"

    def add_days(self, days: int) -> None:
        if days <= 0:
            raise ValueError("Количество дней должно быть положительным")
        self.days_stayed += days

    def calculate_treatment_cost(self) -> float:
        return float(self.daily_rate * self.days_stayed)

    def get_patient_type(self) -> str:
        return "Стационарный пациент"

    def __str__(self) -> str:
        base_str = super().__str__()
        return (f"{base_str}, палата: {self.__ward}, "
                f"дней в стационаре: {self.days_stayed}, "
                f"поступление: {self.admission_date.isoformat()}")

    def __repr__(self) -> str:
        return (f"InpatientPatient(fio={self.fio!r}, age={self.age}, "
                f"diagnosis={self.diagnosis!r}, record_number={self.record_number!r}, "
                f"ward={self.ward}, admission_date={self.admission_date.isoformat()!r})")



class OutpatientPatient(Patient):
    def __init__(self, fio: str, age: int, diagnosis: str, record_number: str | int,
                 next_appointment: date | None = None, 
                 attending_doctor: str | None = None, 
                 insurance_company: str | None = None, 
                 consultation_price: int = 2000) -> None:
        super().__init__(fio, age, diagnosis, record_number)
        self.__next_appointment: date | None = None
        self.__attending_doctor: str | None = None
        self.__insurance_company: str | None = None
        self.next_appointment = next_appointment
        self.attending_doctor = attending_doctor
        self.insurance_company = insurance_company
        self.consultation_price: int = consultation_price
        self.visits_count: int = 0

    @property
    def next_appointment(self) -> date | None:
        return self.__next_appointment

    @next_appointment.setter
    def next_appointment(self, value: date | None) -> None:
        if value is not None and not isinstance(value, date):
            raise TypeError("Дата визита должна быть объектом date или None")
        if value is not None and value < date.today():
            raise ValueError("Дата следующего визита не может быть в прошлом")
        self.__next_appointment = value

    @property
    def attending_doctor(self) -> str | None:
        return self.__attending_doctor

    @attending_doctor.setter
    def attending_doctor(self, value: str | None) -> None:
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("ФИО врача должно быть строкой")
            if not value.strip():
                raise ValueError("ФИО врача не может быть пустым")
            value = value.strip()
        self.__attending_doctor = value

    @property
    def insurance_company(self) -> str | None:
        return self.__insurance_company

    @insurance_company.setter
    def insurance_company(self, value: str | None) -> None:
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("Страховая компания должна быть строкой")
            if not value.strip():
                raise ValueError("Страховая компания не может быть пустой строкой")
            value = value.strip()
        self.__insurance_company = value

    def add_visit(self) -> str:
        if not self.is_active:
            raise RuntimeError("Выписанный пациент не может посещать врача")
        self.visits_count += 1
        return f"Визит #{self.visits_count} зарегистрирован"

    def reschedule_appointment(self, new_date: date) -> str:
        if new_date < date.today():
            raise ValueError("Новая дата не может быть в прошлом")
        old_date = self.__next_appointment
        self.next_appointment = new_date
        return f"Визит перенесён с {old_date} на {new_date}"

    def calculate_treatment_cost(self) -> float:
        return float(self.consultation_price * self.visits_count)

    def get_patient_type(self) -> str:
        return "Амбулаторный пациент"

    def can_prescribe_medicine(self) -> bool:
        if self.age < 21:
            return False
        return super().can_prescribe_medicine()

    def __str__(self) -> str:
        base_str = super().__str__()
        next_date = self.__next_appointment.isoformat() if self.__next_appointment else "не назначен"
        doctor = self.__attending_doctor if self.__attending_doctor else "не назначен"
        insurance = self.__insurance_company if self.__insurance_company else "не указана"
        return (f"{base_str}, следующий визит: {next_date}, "
                f"врач: {doctor}, страховка: {insurance}, "
                f"визитов: {self.visits_count}")

    def __repr__(self) -> str:
        next_appt = self.next_appointment.isoformat() if self.next_appointment else None
        return (f"OutpatientPatient(fio={self.fio!r}, age={self.age}, "
                f"diagnosis={self.diagnosis!r}, record_number={self.record_number!r}, "
                f"next_appointment={next_appt!r}, "
                f"attending_doctor={self.attending_doctor!r}, "
                f"insurance_company={self.insurance_company!r})")