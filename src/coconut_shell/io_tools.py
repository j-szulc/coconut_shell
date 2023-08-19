import sys

from .constants import *
import os

def read_fileobj(fileobj, close=True, block_size=BLOCK_SIZE):
    len_read = 1
    while len_read > 0:
        data = fileobj.read(block_size)
        len_read = len(data)
        if len_read > 0:
            yield data
    if close:
        fileobj.close()

def write_fileobj(fileobj, iterable_data, close=True):
    for data in iterable_data:
        fileobj.write(data)
    if close:
        fileobj.close()

def connect_fileobj(left_fileobj, right_fileobj, close_left=True, close_right=True, block_size=BLOCK_SIZE):
    write_fileobj(right_fileobj, read_fileobj(left_fileobj, close=close_left, block_size=block_size), close=close_right)

def read_fileobj_split(fileobj, separator="\n", close=True):
    buffer = None
    for data in read_fileobj(fileobj, close=close):
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

def print_fileobj(fileobj, close=True):
    buffer = b''
    read_bytes = 0
    for data in read_fileobj(fileobj, close=close, block_size=1):
        buffer += data
        read_bytes += len(data)
        try:
            print(data.decode(), end='')
            sys.stdout.flush()
            buffer = b''
        except UnicodeDecodeError:
            pass
    # print(f"Read {read_bytes} bytes from fileobj", file=sys.stderr)