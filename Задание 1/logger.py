"""Этот модуль предназначен для логирования."""
from typing import Callable, Optional, Any, TypeVar
from functools import wraps


F = TypeVar("F", bound=Callable[..., Any])


def log_operation(func: F) -> F:
    """Декоратор для логирования операций.

    Параметры:
        func (Callable[..., Any]):
        Функция, которую необходимо обернуть декоратором.

    Возвращает:
        Callable[..., Any]: Обернутая функция с добавленным логированием.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Обертка для функции с добавленным логированием.

        Параметры:
            *args (Any): Позиционные аргументы функции.
            **kwargs (Any): Именованные аргументы функции.

        Возвращает:
            Any: Результат выполнения оригинальной функции,
                а также записывает операцию в лог.
        """
        try:
            result = func(*args, **kwargs)
            operation_description =\
                f"Function: {func.__name__} | Args:" \
                f"{args} | Kwargs: {kwargs} | Result: {result}"
            Logger().log(operation_description)
            return result
        except Exception as e:
            error_description =\
                f"Error in function {func.__name__}: {e} | Args:" \
                f"{args} | Kwargs: {kwargs}"
            Logger().log(error_description)
            return error_description
    return wrapper


class Logger:
    """Класс Logger представляет собой синглтон для логирования.

    Этот класс обеспечивает создание только одного экземпляра для логирования.
        Он хранит записанные сообщения и выводит их в консоль,
    когда размер лога превышает определенный предел.

    Атрибуты:
        _instance (Optional[Logger]): Единственный экземпляр класса Logger.
        log_lines (List[str]): Список для хранения записанных сообщений.

    Методы:
        __new__(cls): Переопределяет создание новых экземпляров для
            обеспечения существования только одного экземпляра.
        log(self, message: str): Записывает сообщение в лог и
            выводит его в консоль, если лог превышает 5 строк.
    """

    _instance: Optional["Logger"] = None
    log_lines: list[str]

    def __new__(cls):
        """Функция для обеспечения существования только одного экземпляра.

        Возвращает:
            Logger: Единственный экземпляр класса Logger.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.log_lines = []
        return cls._instance

    def log(self, message: str):
        """Записывает сообщение в лог и выводит его если лог превышает 5 строк.

        Параметры:
            message (str): Сообщение для записи в лог.
        """
        self.log_lines.append(message)
        if len(self.log_lines) >= 5:
            for log_message in self.log_lines:
                print(log_message)
