from datetime import datetime

from bot.utils.logging.models.LogLevel import LogLevel
from bot.utils.logging.models.LogPath import LogPath


class Log:
    def __init__(self, level: LogLevel, message: str, loc: LogPath):
        self.level = level
        self.message = message
        self.loc = loc
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.level.color}{self.level.char} [{self.timestamp}] [{self.loc.path()}] {self.message}"
