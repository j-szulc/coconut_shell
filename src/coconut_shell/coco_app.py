from abc import ABC, abstractmethod

class CocoAppI(ABC):

    @abstractmethod
    def set_input(self, src):
        """Set the input source."""
        pass

    def __call__(self, src):
        """Allows the instance to be called like a function."""
        self.set_input(src)
        return self

class CocoAppO(ABC):

    @abstractmethod
    def get_output(self):
        """Retrieve the output."""
        pass

    def __or__(self, other):
        """Allows the instance to be piped into another using the | operator."""
        if isinstance(other, CocoAppI):
            return cocofy(other)(self.get_output())
        else:
            raise ValueError("The object being piped to is not a valid CocoAppI.")

class CocoAppIO(CocoAppI, CocoAppO):
    pass

class PythonFunction(CocoAppIO):

    def __init__(self, func):
        self.func = func

    def set_input(self, src):
        self.__src = src

    def get_output(self):
        for item in self.__src:
            yield self.func(item)

def cocofy(x):
    if isinstance(x, CocoAppI) or isinstance(x, CocoAppO):
        return x
    else:
        return PythonFunction(x)