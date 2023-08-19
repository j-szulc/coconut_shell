import sys

PIPE = -1

STDIN = sys.stdin.fileno()
STDOUT = sys.stdout.fileno()
STDERR = sys.stderr.fileno()
DEVNULL = -3

BLOCK_SIZE = 4096