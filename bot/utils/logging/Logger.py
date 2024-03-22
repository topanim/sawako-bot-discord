from bot.utils.logging.models.Log import Log
from bot.utils.logging.models.LogLevel import LogLevel
from bot.utils.logging.models.LogPath import LogPath
from bot.utils.logging.static.Levels import Levels


class Logger:

    def __init__(self, loc: str):
        self.__loc = LogPath(loc)

    @classmethod
    def send(
            cls,
            level: LogLevel,
            message: str,
            loc: LogPath = None,
            target: dict = None,
            *args, **kwargs):
        try:
            message = message.format(*args, **target.__dict__, **kwargs)
        except IndexError:
            Logger.base_send(Levels.ERROR, f"Formatting error: There are too many empty cells", loc)
        except KeyError as e:
            Logger.base_send(Levels.ERROR, f"Formatting error: The element `{e.args[0]}` was not found", loc)
        except:
            Logger.base_send(Levels.ERROR, "Unknown formatting error", loc)

        cls.base_send(level, message, loc)

    @staticmethod
    def base_send(level: LogLevel, message: str, loc: LogPath = None):
        if loc is None:
            loc = LogPath()
        log = Log(level, message, loc)
        print(log)

    def n(self, message: str):
        self.base_send(Levels.NOTSET, message, self.__loc)

    def d(self, message: str):
        self.base_send(Levels.DEBUG, message, self.__loc)

    def i(self, message: str):
        self.base_send(Levels.INFO, message, self.__loc)

    def w(self, message: str):
        self.base_send(Levels.WARN, message, self.__loc)

    def e(self, message: str):
        self.base_send(Levels.ERROR, message, self.__loc)

    def c(self, message: str):
        self.base_send(Levels.CRITICAL, message, self.__loc)
