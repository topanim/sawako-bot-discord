from functools import wraps

from bot.utils.logging.Logger import Logger
from bot.utils.logging.models.LogLevel import LogLevel
from bot.utils.logging.models.LogPath import LogPath
from bot.utils.logging.static.Levels import Levels


def log(level: LogLevel = Levels.DEBUG, message: str = ""):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                self.__class__.loc
            except AttributeError as e:
                Logger.base_send(
                    Levels.ERROR,
                    "Config Error: ClassLogger not configured",
                    LogPath().add_class(self).add_func(func))

            Logger.send(
                level,
                message,
                self.__class__.loc.add_class(self).add_func(func),
                self,
                *args,
                **kwargs)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
