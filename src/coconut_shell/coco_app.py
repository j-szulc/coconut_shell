import os
from abc import ABC, abstractmethod
from . import io_tools

class CocoAppI(ABC):

    def __init__(self):
        self.was_input_set = False

    @abstractmethod
    def _set_input(self, src):
        """Set the input source."""
        pass

    def __call__(self, src):
        """Allows the instance to be called like a function."""
        self._set_input(src)
        return self

class CocoAppO(ABC):

    def __init__(self):
        self.was_output_get = False

    @abstractmethod
    def _get_output(self):
        """Retrieve the output."""
        pass

    def __or__(self, other):
        """Allows the instance to be piped into another using the | operator."""
        assert not self.was_output_get
        self.was_output_get = True
        if isinstance(other, CocoAppI):
            return cocofy(other)(self._get_output())
        else:
            raise ValueError("The object being piped to is not a valid CocoAppI.")

class CocoAppIO(CocoAppI, CocoAppO):

    def __init__(self):
        CocoAppI.__init__(self)
        CocoAppO.__init__(self)

def lines(src):
    if isinstance(src, str) or isinstance(src, bytes):
        return src.splitlines()
    else:
        try:
            try:
                yield from io_tools.read_fileobj_split(src, separator="\n", close=True)
            except TypeError:
                yield from io_tools.read_fileobj_split(src, separator=b"\n", close=True)
        except AttributeError:
            yield from src

class CocoIterable(CocoAppO):

    def __init__(self, obj):
        super().__init__()
        self.obj = obj

    def _get_output(self):
        return self.obj

    def __iter__(self):
        return iter(self.obj)

    def __repr__(self):
        return repr(self.obj)

    def __getitem__(self, item):
        return self.obj[item]


class PythonFunction(CocoAppIO):

    def __init__(self, func):
        super().__init__()
        self.func = func

    def _set_input(self, src):
        self.src = src

    def __get_output(self):
        for item in lines(self.src):
            yield self.func(item)

    def _get_output(self):
        return CocoIterable(self.__get_output())

def cocofy(x):
    if isinstance(x, CocoAppI) or isinstance(x, CocoAppO):
        return x
    elif callable(x):
        return PythonFunction(x)
    else:
        return x

