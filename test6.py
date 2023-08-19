import os
import subprocess as sp

def f():
    r, w = os.pipe()

    a = sp.Popen(["seq", "10000000"], stdout=w)
    b = sp.Popen(["wc","-l"], stdin=r, stdout=sp.PIPE)
    os.close(w)
    output = b.communicate()[0]
    print(output.decode())