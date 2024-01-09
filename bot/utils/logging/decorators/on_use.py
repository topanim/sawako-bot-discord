from bot.utils.logging.Level import Level
from bot.utils.logging.Log import Log


# TODO: Fix errors in cogs

def on_use(logger: Log, level: Level, mess: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if mess:
                logger.log(level, mess)
            else:
                logger.log(level, func.__name__)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def async_on_use(logger: Log, level: Level, mess: str = None):
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            if mess:
                logger.log(level, mess)
            else:
                logger.log(level, func.__name__)
            return func(*args, **kwargs)

        return wrapper

    return decorator
