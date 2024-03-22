from bot.utils.logging.decorators.ClassLogger import ClassLogger
from bot.utils.logging.decorators.Informer import log
from bot.utils.logging.decorators.InputLog import input_log
from bot.utils.logging.decorators.OutputLog import output_log
from bot.utils.logging.static.Levels import Levels


@ClassLogger(__file__)
class Person:

    def __init__(self, name: str):
        self.name = name

    @log(message="{text} {name} said {person}")
    @input_log()
    @output_log()
    def call(self, text: str, person: str):
        # do something
        pass


s = Person("John")
s.call(text="hi", person="Nick")
