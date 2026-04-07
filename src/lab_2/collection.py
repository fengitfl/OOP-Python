from models import Patient

class PatientList:

    def __init__(self):
        self._patients = []

    def add(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только Patient, получен {type(patient).__name__}")
        for p in self._patients:
            if p.record_number == patient.record_number:
                raise ValueError(f"Пациент с номером {patient.record_number} уже существует")

        self._patients.append(patient)

    def remove(self, patient):
        if patient not in self._patients:
            raise ValueError("Такого пациента нет в коллекции")
        self._patients.remove(patient)

    def remove_at(self, index):
        if index < 0 or index >= len(self._patients):
            raise IndexError("Индекс вне диапазона")
        del self._patients[index]

    def get_all(self):
        return self._patients.copy()

    #Магические методы  
    def __len__(self):
        return len(self._patients)

    def __iter__(self):
        return iter(self._patients)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
    
        # Преобразуем отрицательный индекс в положительный
        length = len(self._patients)
        if index < 0:
            index = length + index
    
        if index < 0 or index >= length:
            raise IndexError("Индекс вне диапазона")
        return self._patients[index]

    # Поиск 
    def find_by_fio(self, fio_part):
        result = [p for p in self._patients if fio_part.lower() in p.fio.lower()]
        if not result:
            raise ValueError(f"Пациенты с ФИО, содержащим '{fio_part}', не найдены")
        return result

    def find_by_id(self, record_id):
        for patient in self._patients:
            if patient.record_number == str(record_id):
                return patient
        raise ValueError(f"Пациент с номером {record_id} не найден")

    def find_by_diagnosis(self, diagnosis):
        result = [p for p in self._patients if diagnosis.lower() in p.diagnosis.lower()]
        if not result:
            raise ValueError(f"Пациенты с диагнозом, содержащим '{diagnosis}', не найдены")
        return result

    #Сортировка 
    def sort_by_fio(self, reverse=False):
        self._patients.sort(key=lambda p: p.fio, reverse=reverse)

    def sort_by_age(self, reverse=False):
        self._patients.sort(key=lambda p: p.age, reverse=reverse)

    def sort_by_record_number(self, reverse=False):
        self._patients.sort(key=lambda p: p.record_number, reverse=reverse)

    # Фильтрация (логические операции)
    def filter(self, predicate):
        new_collection = PatientList()
        for patient in self._patients:
            if predicate(patient):
                new_collection.add(patient)
        return new_collection

    def get_active(self):
        return self.filter(lambda p: p.is_active)

    def get_discharged(self):
        return self.filter(lambda p: not p.is_active)

    def get_adults(self):
        return self.filter(lambda p: p.age >= 18)

    def get_by_min_age(self, min_age):
        return self.filter(lambda p: p.age >= min_age)