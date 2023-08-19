import shlex
import os
import subprocess as sp
import threading
from .constants import *
from .io_tools import *
from .coco_app import *

class Subprocess(CocoAppIO):

    def __init__(self, command, stdin=PIPE, stdout=PIPE, stderr=DEVNULL, shell=False):
        super().__init__()

        assert stdin in (PIPE, DEVNULL)
        assert stdout in (PIPE, DEVNULL)
        assert stderr in (PIPE, DEVNULL)

        if isinstance(command, str) and not shell:
            command = shlex.split(command)

        self.sp = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.was_stdout_get = False
        self.was_input_set = False

    def _get_output(self):
        assert self.stdout == PIPE
        assert not self.was_stdout_get
        self.was_stdout_get = True
        return self.sp.stdout

    def _set_input(self, src):
        assert self.stdin is not None
        assert not self.was_input_set
        self.was_input_set = True
        self.set_input_thread = threading.Thread(target=connect_fileobj, args=(src, self.sp.stdin))
        self.set_input_thread.start()
