from src.lab_1.models import Patient

class PatientList:
    def __init__(self):
        self._patients = []
    
    def add(self, obj):
        if isinstance(obj, Patient):
            self._patients.add(obj)
        else:
            raise TypeError(f"Только класс Пациент можно добавлять, вы же добавляете {type(obj).__name__}")
        
    def remove(self, patient):
        self._patients.remove(patient)
    
    def get_all(self):
        return self._patients
    
    def __iter__(self):
        return iter(self._patients)
    
    def len(self):
        return len(self._patients)
    
    def find_by_fio(self, fio_part: str):
        found_fio = []
        for patient in self._patients:
            if fio_part in patient.fio:
                found_fio.append(patient)
        if not found_fio:
            raise ValueError(f"Такого пациента нет, имя или фамилия были указаны неправильно")
        return found_fio
    
    def find_by_id(self, id: str):
        found_id = []
        for patient in self._patients:
            if patient.record_numder == id:
                found_id.append(patient)
        if not found_id:
            raise ValueError(f"Пациента с таким номером нет")
        return found_id
    
