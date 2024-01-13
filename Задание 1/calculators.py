"""Этот модуль включает в себя реализацию системы калькулятора."""
from abc import ABC, abstractmethod
from logger import log_operation
from typing import Union, Callable


class Calculator(ABC):
    """Абстрактный класс Calculator.

    Абстрактный класс Calculator предоставляет интерфейс для калькуляторов.

    Методы:
        calculate(self, operator: str, *args) -> float:
            Абстрактный метод для выполнения операции калькулятора.
    """
    @abstractmethod
    def calculate(self, operator: str, *args) -> float:
        pass


class SimpleCalculator(Calculator):
    """Класс простого калькулятора.

    Класс SimpleCalculator представляет собой простой калькулятор,
        реализующий интерфейс Calculator.

    Атрибуты:
        operators (dict): Словарь операторов и
            соответствующих им функций.

    Методы:
        calculate(self, operator: str, *args) -> float:
            Выполняет операцию калькулятора.
    """
    def __init__(self):
        self.operators: dict[str, Callable[..., Union[float, int]]] = {
            '+': self.sequential_operation(lambda a, b: a + b),
            '-': self.sequential_operation(lambda a, b: a - b),
            '*': self.sequential_operation(lambda a, b: a * b),
            '**': self.sequential_operation(lambda a, b: a ** b),
            '/': self.sequential_operation(lambda a, b: a / b),
            '//': self.sequential_operation(lambda a, b: a // b),
            '%': self.sequential_operation(lambda a, b: a % b)
        }

    def sequential_operation(self, operation: Callable[[float, float], float])\
            -> Callable[..., Union[float, int]]:
        def apply_operation(*args: float) -> Union[float, int]:
            result: float = args[0]
            for arg in args[1:]:
                result = operation(result, arg)
            return result
        return apply_operation

    @log_operation
    def calculate(self, operator: str, *args) -> Union[float, int]:
        """
        Выполняет операцию калькулятора.

        Параметры:
            operator (str): Оператор для выполнения.
            *args: Аргументы операции.

        Возвращает:
            Union[float, int]: Результат операции.
        """
        if not operator in self.operators:
            raise ValueError("Неверный оператор.")
        elif len(args) < 2:
            raise ValueError("Неправильное количество аргументов.")
        else:
            return self.operators[operator](*args)



class Calculators:
    """
    Класс Calculators предоставляет фабричный метод для создания различных типов калькуляторов.

    Методы:
    - get_calculator(type: str) -> Calculator: Возвращает экземпляр калькулятора по указанному типу.
    """
    @staticmethod
    def get_calculator(type: str) -> Calculator:
        """
        Возвращает экземпляр калькулятора по указанному типу.

        Параметры:
            type (str): Тип калькулятора.

        Возвращает:
            Calculator: Экземпляр калькулятора.
        """
        match type:
            case "simple":
                return SimpleCalculator()
            case _:
                raise ValueError("Неизвестный тип калькулятора")
