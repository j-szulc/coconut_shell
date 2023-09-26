import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from . import coco_app
from . import _subprocess
from . import io_tools
import os, pathlib

def sh(*args, **kwargs):
    return _subprocess.Subprocess(*args, **kwargs)

class Cat(coco_app.CocoAppI):

    def __init__(self):
        super().__init__()

    def _set_input(self, *srcs):
       for src in srcs:
              for line in lines(src):
                print(line)

    def __repr__(self):
        return None

cat = Cat()

lines = coco_app.lines

class Grep(coco_app.CocoAppIO):

    def __init__(self, pattern, invert=False):
        super().__init__()
        self.pattern = pattern
        self.invert = invert

    def _set_input(self, src):
        self.src = src

    def __get_output(self):
        for line in lines(self.src):
            if (self.pattern in line) ^ self.invert:
                yield line

    def _get_output(self):
        return coco_app.CocoIterable(self.__get_output())


class BetterPath(pathlib.Path):

    def __iter__(self):
        return iter(self.name + self.suffix)

BetterPath._flavour = pathlib._windows_flavour if os.name == "nt" else pathlib._posix_flavour


def grep(pattern, invert=False):
    return Grep(pattern, invert=invert)

def ls(path="."):
    path = os.path.expanduser(path)
    return coco_app.CocoIterable([BetterPath(path) / f for f in os.listdir(path)])

