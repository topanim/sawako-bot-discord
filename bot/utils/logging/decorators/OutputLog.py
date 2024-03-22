from functools import wraps

from bot.utils.logging.Logger import Logger
from bot.utils.logging.models.LogLevel import LogLevel
from bot.utils.logging.static.Levels import Levels


def output_log(level: LogLevel = Levels.DEBUG):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            Logger.base_send(
                level,
                f"[*Input] Args: {args}, KwArgs: {kwargs}]",
                self.__class__.loc.add_class(self).add_func(func)
            )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
