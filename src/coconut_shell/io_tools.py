from .constants import *
import logging
import os

def setup_logger(pipe_fd, level, name=None):
    level = {
        LOGGER_DEBUG: logging.DEBUG,
        LOGGER_INFO: logging.INFO,
        LOGGER_WARNING: logging.WARNING,
        LOGGER_ERROR: logging.ERROR,
        LOGGER_CRITICAL: logging.CRITICAL,
    }[level]
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler(os.fdopen(pipe_fd, 'w'))
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(log_formatter)
    if name:
        handler.set_name(name)
    logger.addHandler(handler)
    return logger

def fd_read(fd, close=True, block_size=BLOCK_SIZE):
    len_read = 1
    while len_read > 0:
        data = os.read(fd, block_size)
        len_read = len(data)
        if len_read > 0:
            yield data
    if close:
        os.close(fd)

def fd_write(fd, iterable_data, close=True):
    for data in iterable_data:
        os.write(fd, data)
    if close:
        os.close(fd)

def connect_pipes(left_fd, right_fd, close_left=True, close_right=True, block_size=BLOCK_SIZE):
    fd_write(right_fd, fd_read(left_fd, close=close_left, block_size=block_size), close=close_right)

def fd_read_split(fd, separator="\n", close=True):
    buffer = None
    for data in fd_read(fd, close=close):
        index = data.find(separator)
        while index >= 0:
            if buffer is None:
                yield data[:index]
            else:
                yield buffer + data[:index]
                buffer = None
            data = data[index + len(separator):]
            index = data.find(separator)
        if buffer is None:
            buffer = data
        else:
            buffer += data

def fd_print(fd, close=True):
    buffer = b''
    for data in fd_read(fd, close=close, block_size=1):
        buffer += data
        try:
            print(data.decode(), end='')
            buffer = b''
        except UnicodeDecodeError:
            pass

class OsNonblockFdopen:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.obj = None

    def __get_obj(self):
        if self.obj is None:
            self.obj = os.fdopen(*self.args, **self.kwargs)
        return self.obj

    def __enter__(self):
        return self.__get_obj().__enter__()

    def __exit__(self):
        return self.__get_obj().__exit__()

    def fileno(self):
        return self.__get_obj().fileno()
