from colorama import Fore

from bot.utils.logging.models.LogLevel import LogLevel


class Levels:
    NOTSET = LogLevel(Fore.WHITE, '//')
    DEBUG = LogLevel(Fore.BLUE, '#')
    INFO = LogLevel(Fore.GREEN, 'I')
    WARN = LogLevel(Fore.LIGHTYELLOW_EX, '*')
    ERROR = LogLevel(Fore.RED, '!')
    CRITICAL = LogLevel(Fore.LIGHTMAGENTA_EX, '!!')