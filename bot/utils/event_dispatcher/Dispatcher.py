from json import loads, dumps

from disnake import Embed

from bot.utils.logging.Log import Log
from bot.utils.logging.decorators.on_error import on_error

logger = Log(__file__)


class Dispatcher:

    @classmethod
    @on_error(logger, Log.ERROR)
    async def dispatch(cls, channel, send_obj: dict, data: dict):
        await channel.send(
            content=cls.ParsedText(send_obj['text'], params=data),
            embed=cls.ParsedEmbed(send_obj['embed'], params=data))

    @classmethod
    def ParsedEmbed(cls, obj: dict, params: dict) -> Embed | None:
        if obj['flag']:
            return Embed.from_dict(loads(dumps(cls.format_dict(obj['entity'], params))))

    @classmethod
    def ParsedText(cls, obj: dict, params: dict) -> str | None:
        if obj['flag']:
            return obj['content'].format(**params)

    @classmethod
    def format_dict(cls, obj: dict, data: dict):
        for key, val in obj.items():
            if isinstance(val, str):
                obj[key] = obj[key].format(**data)
            elif isinstance(val, dict):
                obj[key] = cls.format_dict(obj[key], data)
            elif isinstance(val, list):
                obj[key] = [cls.format_dict(it, data) for it in obj[key]]
        return obj
