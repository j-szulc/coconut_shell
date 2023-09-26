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

    def set_input(self, src):
        """Set the input source."""
        assert not self.was_input_set
        self._set_input(src)
        self.was_input_set = True

    def __call__(self, src):
        """Allows the instance to be called like a function."""
        self.set_input(src)
        return self

class CocoAppO(ABC):

    def __init__(self):
        self.was_output_get = False

    @abstractmethod
    def _get_output(self):
        """Retrieve the output."""
        pass

    def get_output(self):
        """Retrieve the output."""
        assert not self.was_output_get
        result = self._get_output()
        self.was_output_get = True
        return result

    def __or__(self, other):
        """Allows the instance to be piped into another using the | operator."""
        return cocofy(other)(self.get_output())

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


class InvalidCocoAppError(Exception):
    pass

def cocofy(x):
    if isinstance(x, CocoAppI) or isinstance(x, CocoAppO):
        return x
    if callable(x):
        return PythonFunction(x)
    raise InvalidCocoAppError(f"Cannot cocofy {x} of type {type(x)}")
