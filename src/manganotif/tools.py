from functools import wraps
from .core.errors import RequiredAttributeError


def required(func):
    """
    Декоратор, который проверяет, что декорируемая функция возвращает значение, отличное от None.

    Если функция возвращает None, пустой список, False или любое «ложное» значение,
    вызывается исключение RequiredAttributeError. Используется для обозначения методов,
    которые обязательно должны вернуть значимый результат (например, парсинг критичных данных).

    Применяется к методам парсеров, где отсутствие результата означает сбой или
    критическую ошибку в логике (например, не найдены ожидаемые элементы на странице).

    Args:
        func (Callable): Функция, которую необходимо обернуть. Должна возвращать
            значимое значение (не None и не пустое).

    Returns:
        Callable: Обёрнутая функция, выбрасывающая исключение при ложном результате.

    Raises:
        RequiredAttributeError: Если результат выполнения функции является «ложным»
            (например, None, [], {}, False, "" и т.п.).

    Example:
        @required
        def parse_title(soup):
            title = soup.find('h1')
            return title.get_text() if title else None

        # Если title не найден, будет вызвано исключение:
        # RequiredAttributeError: Обязательная функция вернула ничего (func_name=parse_title)

    Note:
        Декоратор использует `not result`, поэтому учтите, что ложные значения
        вроде `False`, `0`, `""` также вызовут исключение. Если ожидается
        возможность таких значений — используйте проверку `result is None` отдельно.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            raise RequiredAttributeError(
                f"Обязательная функция вернула ничего (func_name={func.__name__})"
            )
        return result

    return wrapper
