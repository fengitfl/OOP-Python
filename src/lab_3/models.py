from datetime import date
from base import Patient

class InpatientPatient(Patient):
    def __init__(self, fio, age, diagnosis, record_number, ward, admission_date=None, daily_rate=5000):
        super().__init__(fio, age, diagnosis, record_number)
        self.ward = ward
        self.admission_date = admission_date if admission_date else date.today()
        self.daily_rate = daily_rate
        self.days_stayed = 0

    @property
    def ward(self):
        return self.__ward

    @ward.setter
    def ward(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номер палаты должен быть положительным целым числом")
        self.__ward = value

    def change_ward(self, new_ward):
        if not self.is_active:
            raise RuntimeError("Нельзя перевести выписанного пациента")
        old_ward = self.__ward
        self.ward = new_ward
        return f"Пациент переведён из палаты {old_ward} в палату {new_ward}"

    def add_days(self, days):
        if days <= 0:
            raise ValueError("Количество дней должно быть положительным")
        self.days_stayed += days

    def calculate_treatment_cost(self):
        return self.daily_rate * self.days_stayed

    def get_patient_type(self):
        return "Стационарный пациент"

    def __str__(self):
        base_str = super().__str__()
        return (f"{base_str}, палата: {self.__ward}, "
                f"дней в стационаре: {self.days_stayed}, "
                f"поступление: {self.admission_date.isoformat()}")

    def __repr__(self):
        return (f"InpatientPatient(fio={self.fio!r}, age={self.age}, "
                f"diagnosis={self.diagnosis!r}, record_number={self.record_number!r}, "
                f"ward={self.ward}, admission_date={self.admission_date.isoformat()!r})")


class OutpatientPatient(Patient):
    def __init__(self, fio, age, diagnosis, record_number, next_appointment=None, 
                 attending_doctor=None, insurance_company=None, consultation_price=2000):
        super().__init__(fio, age, diagnosis, record_number)
        self.next_appointment = next_appointment
        self.attending_doctor = attending_doctor
        self.insurance_company = insurance_company
        self.consultation_price = consultation_price
        self.visits_count = 0

    @property
    def next_appointment(self):
        return self.__next_appointment

    @next_appointment.setter
    def next_appointment(self, value):
        if value is not None and not isinstance(value, date):
            raise TypeError("Дата визита должна быть объектом date или None")
        if value is not None and value < date.today():
            raise ValueError("Дата следующего визита не может быть в прошлом")
        self.__next_appointment = value

    @property
    def attending_doctor(self):
        return self.__attending_doctor

    @attending_doctor.setter
    def attending_doctor(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("ФИО врача должно быть строкой")
            if not value.strip():
                raise ValueError("ФИО врача не может быть пустым")
            value = value.strip()
        self.__attending_doctor = value

    @property
    def insurance_company(self):
        return self.__insurance_company

    @insurance_company.setter
    def insurance_company(self, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("Страховая компания должна быть строкой")
            if not value.strip():
                raise ValueError("Страховая компания не может быть пустой строкой")
            value = value.strip()
        self.__insurance_company = value

    def add_visit(self):
        if not self.is_active:
            raise RuntimeError("Выписанный пациент не может посещать врача")
        self.visits_count += 1
        return f"Визит #{self.visits_count} зарегистрирован"

    def reschedule_appointment(self, new_date):
        if new_date < date.today():
            raise ValueError("Новая дата не может быть в прошлом")
        old_date = self.__next_appointment
        self.next_appointment = new_date
        return f"Визит перенесён с {old_date} на {new_date}"

    def calculate_treatment_cost(self):
        return self.consultation_price * self.visits_count

    def get_patient_type(self):
        return "Амбулаторный пациент"

    def can_prescribe_medicine(self):
        if self.age < 21:
            return False
        return super().can_prescribe_medicine()

    def __str__(self):
        base_str = super().__str__()
        next_date = self.__next_appointment.isoformat() if self.__next_appointment else "не назначен"
        doctor = self.__attending_doctor if self.__attending_doctor else "не назначен"
        insurance = self.__insurance_company if self.__insurance_company else "не указана"
        return (f"{base_str}, следующий визит: {next_date}, "
                f"врач: {doctor}, страховка: {insurance}, "
                f"визитов: {self.visits_count}")
    def __repr__(self):
        next_appt = self.next_appointment.isoformat() if self.next_appointment else None
        return (f"OutpatientPatient(fio={self.fio!r}, age={self.age}, "
            f"diagnosis={self.diagnosis!r}, record_number={self.record_number!r}, "
            f"next_appointment={next_appt!r}, "
            f"attending_doctor={self.attending_doctor!r}, "
            f"insurance_company={self.insurance_company!r})")

