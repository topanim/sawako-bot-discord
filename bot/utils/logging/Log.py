from datetime import datetime
from colorama import Fore

from bot.utils.logging.Level import Level


class Log:
    NOTSET = Level(Fore.WHITE, '//')
    DEBUG = Level(Fore.BLUE, '#')
    INFO = Level(Fore.GREEN, 'I')
    WARN = Level(Fore.LIGHTYELLOW_EX, '*')
    ERROR = Level(Fore.RED, '!')
    CRITICAL = Level(Fore.LIGHTMAGENTA_EX, '!!')

    def __init__(self, filename: str):
        self.file = '..\\' + '\\'.join(filename.split('\\')[-3:])

    def log(self, level: Level, text: str):
        print(level.color + level.char, f'[{datetime.now()}]', f'[{self.file}]', text)

    def n(self, text: str):
        print(Log.NOTSET.color + self.NOTSET.char, f'[{datetime.now()}]', f'[{self.file}]', text)

    def d(self, text: str):
        print(Log.DEBUG.color + self.DEBUG.char, f'[{datetime.now()}]', f'[{self.file}]', text)

    def i(self, text: str):
        print(Log.INFO.color + self.INFO.char, f'[{datetime.now()}]', f'[{self.file}]', text)

    def w(self, text: str):
        print(Log.WARN.color + self.WARN.char, f'[{datetime.now()}]', f'[{self.file}]', text)

    def e(self, text: str):
        print(Log.ERROR.color + self.ERROR.char, f'[{datetime.now()}]', f'[{self.file}]', text)

    def c(self, text: str):
        print(Log.CRITICAL.color + self.CRITICAL.char, f'[{datetime.now()}]', f'[{self.file}]', text)
