import subprocess
import shlex
import threading

DEVNULL = -3
STDOUT = -2
PIPE = -1


def fork(function, *args, **kwargs):
    t = threading.Thread(target=function, args=args, kwargs=kwargs)
    t.start()
    return t


class Subprocess:

    @staticmethod
    def __inputFeeder(inputFrom, inputTo):
        for line in inputFrom:
            if inputTo.writable():
                inputTo.write((line + "\n").encode("utf-8"))
                inputTo.flush()
            else:
                break
        inputTo.close()

    @staticmethod
    def __outputHandler(outputFrom):
        for line in outputFrom:
            yield line.decode("utf-8").rstrip()

    def __setupInput(self, inputSource):
        self.stdinFeeder = fork(Subprocess.__inputFeeder, inputSource, self.process.stdin)

    def __init__(self, command,  stdout=PIPE, stderr=None, shell=False):

        ## We don't know if there's input, because it may be provided by __call__ after the __init__
        ## Thus

        stdin = PIPE

        if shell:
            self.process = subprocess.Popen(command,
                                            stdin=stdin,
                                            stdout=stdout,
                                            stderr=stderr,
                                            shell=True
                                            )
        else:
            self.process = subprocess.Popen(shlex.split(command),
                                            stdin=stdin,
                                            stdout=stdout,
                                            stderr=stderr,
                                            shell=False)

        #if inputSource is not None:
        #    self.__setupInput(inputSource)

        if stdout is PIPE:
            self.stdout = Subprocess.__outputHandler(self.process.stdout)

        if stderr is PIPE:
            self.stderr = Subprocess.__outputHandler(self.process.stderr)

    def __next__(self):
        return next(self.stdout)

    def __iter__(self):
        return self

    def __call__(self,inputSource):
        self.__setupInput(inputSource)
        return self

    ## uncomment to make __repr__ dump stdout automatically
    ## e.g.
    ## sh("ls")
    ## will print the file list instead of
    ## <__main__.Subprocess object at 0x123456789abc>

    # def __repr__(self):
    #    fork(cat,self)
    #    return ""

def sh(*args, **kwargs):
    return Subprocess(*args, **kwargs)

def cat(iterable):
    for line in iterable:
        print(line)

def void(iterable):
    for line in iterable:
        pass