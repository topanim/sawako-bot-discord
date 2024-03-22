from functools import wraps

from bot.utils.logging.Logger import Logger
from bot.utils.logging.models.LogLevel import LogLevel
from bot.utils.logging.static.Levels import Levels


def input_log(level: LogLevel = Levels.DEBUG):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            Logger.base_send(
                level,
                f"[*Output] Result: {res}",
                self.__class__.loc.add_class(self).add_func(func)
            )

            return res

        return wrapper

    return decorator
