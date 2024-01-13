"""Главный модуль для."""
from calculators import Calculators


def main():
    """Функция функция для демонстрации работы калькулятора."""
    calculator = Calculators.get_calculator("simple")
    result = calculator.calculate('+', 2, 2)
    print(result)


if __name__ == "__main__":
    main()
