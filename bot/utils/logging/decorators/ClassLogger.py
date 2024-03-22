from bot.utils.logging.models.LogPath import LogPath


def ClassLogger(loc: str):
    def decorator(cls):
        cls.loc = LogPath().add_loc(loc)
        return cls
    return decorator



