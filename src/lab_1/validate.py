def validate_name(value: str):
    """Проверяет, что имя — непустая строка."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Имя должно быть непустой строкой")

def validate_age(value: int):
    """Проверяет возраст: целое число от 0 до 120."""
    # type(value) is int — строгая проверка, чтобы отсечь bool
    if type(value) is not int:
        raise TypeError("Возраст должен быть целым числом")
    if value < 0 or value > 120:
        raise ValueError("Возраст должен быть в диапазоне 0–120")

def validate_diagnosis(value: str):
    """Проверяет диагноз: строка (может быть пустой)."""
    if not isinstance(value, str):
        raise TypeError("Диагноз должен быть строкой")

def validate_record_number(value):
    """Проверяет номер карты: непустая строка или число."""
    if not isinstance(value, (str, int)):
        raise TypeError("Номер карты должен быть строкой или числом")
    if str(value).strip() == "":
        raise ValueError("Номер карты не может быть пустым")