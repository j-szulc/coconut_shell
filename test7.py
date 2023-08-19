
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

x = sh(">&2 echo error",shell=True,stderr=PIPE)
print_fileobj(x.sp.stdout)
print_fileobj(x.sp.stderr)