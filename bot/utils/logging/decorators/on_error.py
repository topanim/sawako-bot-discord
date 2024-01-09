from bot.utils.logging.Log import Log, Level


def on_error(logger: Log, level: Level, mess: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if mess:
                    logger.log(level, mess)
                else:
                    logger.log(level, f'{e.__class__.__name__}: {e}')
        return wrapper
    return decorator
