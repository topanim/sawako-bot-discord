class LogPath:
    __loc: str = None
    __cls: str = None
    __func: str = None

    def add_loc(self, loc):
        self.__loc = loc
        return self

    def add_class(self, cls):
        self.__cls = cls.__class__.__name__
        return self

    def add_func(self, func: str):
        self.__func = func.__name__
        return self

    def path(self, last: int = 3):
        res = ''
        if self.__loc is not None:
            res += '..\\' + '\\'.join(self.__loc.split('\\')[-last:])
        if self.__cls is not None:
            res += f"::{self.__cls}"
        if self.__func is not None:
            res += f"\\{self.__func}"

        return res
