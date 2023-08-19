
from coconut_shell import sh, echo
from coconut_shell.constants import *
from coconut_shell.io_tools import *
import os
import psutil

# p = sh(["seq", "10000000"])
# q = sh(["wc", "-l"])
# p | q | echo

# fd_r, fd_w = os.pipe()
# p = sh("seq 1000")
# os.close(p.st)

x = sh("sh -c 'echo hello world >&2'",shell=True,stderr=PIPE)
fd_print(x.stderr_r)

