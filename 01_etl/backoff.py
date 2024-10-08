import logging
from functools import wraps
from time import sleep
from typing import Callable

_logger = logging.getLogger(__name__)


def backoff(
        exceptions: list[Exception],
        start_sleep_time: float = 0.1,
        factor: int = 2,
        border_sleep_time: float = 10,
        excp_logger: Callable[[], None] = lambda: _logger.exception(
            "Execution problems")
):
    """
    Repeat 'func' with increasing timeout after occured exception

    Formula:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param exceptions
    :param start_sleep_time:
    :param factor:
    :param border_sleep_time:
    :param excp_logger: exception logging
    :return: function result
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            i = 0
            j = input("Максимальное кол-во запусков: ")
            while i<j:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions):
                    excp_logger()
                sleep_time = start_sleep_time * factor ** i
                sleep(sleep_time if sleep_time < border_sleep_time
                      else border_sleep_time)
                i += 1

        return inner

    return func_wrapper
