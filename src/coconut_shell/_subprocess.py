import shlex
import os
import subprocess as sp
import threading
from .constants import *
from .io_tools import *
from .coco_app import *

class Subprocess(CocoAppIO):

    def __init__(self, command, stdin=PIPE, stdout=PIPE, stderr=LOGGER_WARNING, shell=False):

        assert stdin in (PIPE, DEVNULL, STDIN)
        if stdin == PIPE:
            self.was_input_set = False
            self.stdin_r, self.stdin_w = os.pipe()
            stdin = self.stdin_r
        else:
            self.stdin_r = None
            self.stdin_w = None

        assert stdout in (PIPE, DEVNULL, STDOUT, STDERR, *LOGGERS)
        if stdout in (PIPE, *LOGGERS):
            self.stdout_r, self.stdout_w = os.pipe()
            self.was_stdout_get = False
            if stdout in LOGGERS:
                self.was_stdout_get = True
                setup_logger(self.stdout_r, stdout)
            stdout = self.stdout_w
        else:
            self.stdout_r = None
            self.stdout_w = None

        assert stderr in (PIPE, DEVNULL, STDOUT, STDERR, *LOGGERS)
        if stderr in (PIPE, *LOGGERS):
            self.stderr_r, self.stderr_w = os.pipe()
            if stderr in LOGGERS:
                setup_logger(self.stderr_r, stderr)
            stderr = OsNonblockFdopen(self.stderr_w, "wb")
        else:
            self.stderr_r = None
            self.stderr_w = None

        if isinstance(command, str):
            command = shlex.split(command)

        self.sp = sp.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)
        for maybe_fd in [self.stdin_r, self.stdout_w, self.stderr_w]:
            if maybe_fd is not None:
                os.close(maybe_fd)

    def get_output(self):
        assert self.stdout_r is not None
        assert not self.was_stdout_get
        self.was_stdout_get = True
        return self.stdout_r

    def set_input(self, src):
        assert self.stdin_w is not None
        assert not self.was_input_set
        self.was_input_set = True
        if not isinstance(src, int):
            src = src.file_no()
        self.set_input_thread = threading.Thread(target=connect_pipes, args=(src, self.stdin_w))
        self.set_input_thread.start()

class Echo(CocoAppI):

    def set_input(self, src_fd):
        connect_pipes(src_fd, STDOUT, close_right=False)

echo = Echo()