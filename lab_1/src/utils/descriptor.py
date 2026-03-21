from typing import Union


class ValidatedNumber:
    """
    Дескриптор для инкапсуляции логики валидации числовых атрибутов.
    Защищает от установки отрицательных значений цены, количества или баланса.
    """

    def __init__(self, min_value: Union[int, float] = 0, allow_zero: bool = True):
        self.min_value = min_value
        self.allow_zero = allow_zero
        self.name = None

    def __set_name__(self, owner, name: str) -> None:
        # Автоматически вызывается при создании класса-владельца
        # Сохраняем значение в защищенный атрибут (например, _price)
        self.name = f"_{name}"

    def __get__(self, instance, owner) -> Union[int, float]:
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value: Union[int, float]) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Значение для атрибута '{self.name.lstrip('_')}' должно быть числом.")
        
        if not self.allow_zero and value <= self.min_value:
            raise ValueError(
                f"Значение '{self.name.lstrip('_')}' должно быть строго больше {self.min_value}. "
                f"Получено: {value}"
            )
            
        if self.allow_zero and value < self.min_value:
            raise ValueError(
                f"Значение '{self.name.lstrip('_')}' не может быть меньше {self.min_value}. "
                f"Получено: {value}"
            )
            
        setattr(instance, self.name, value) 