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

def sh(*args, **kwargs):
    return _subprocess.Subprocess(*args, **kwargs)

class Echo(coco_app.CocoAppI):

    def _set_input(self, src):
       io_tools.print_fileobj(src)

echo = Echo()
