import subprocess
import shlex
import threading
import collections

DEVNULL = -3
STDOUT = -2
PIPE = -1

## Custom modes

# Equivalent to None in the subprocess library
# e.g. if stderr is PASSTHROUGH then any errors from the slave process
# will get dumped as if they were master's process errors
# (i.e. slave.stderr -> master.stderr)
PASSTHROUGH = -4

# Implies PIPE in the underlying subprocess call
# but disables this library from doing anything to that output
# i.e. it can be read directly from Subprocess.process
# e.g. output = Subprocess.process.stdout.read()
# hence RAW
RAW = -5

customModes = {
    PASSTHROUGH: None,
    RAW: PIPE
}


def toSpArgument(mode):
    if mode in customModes:
        return customModes[mode]
    else:
        return mode


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

    def __init__(self, command, stdout=PIPE, stderr=PASSTHROUGH, shell=False):

        ## We don't know if there's input, because it may be provided by __call__ after the __init__
        ## Thus

        stdin = PIPE

        if shell:
            self.process = subprocess.Popen(command,
                                            stdin=toSpArgument(stdin),
                                            stdout=toSpArgument(stdout),
                                            stderr=toSpArgument(stderr),
                                            shell=True
                                            )
        else:
            self.process = subprocess.Popen(shlex.split(command),
                                            stdin=toSpArgument(stdin),
                                            stdout=toSpArgument(stdout),
                                            stderr=toSpArgument(stderr),
                                            shell=False)

        # if inputSource is not None:
        #    self.__setupInput(inputSource)

        if stdout is PIPE:
            self.stdout = Subprocess.__outputHandler(self.process.stdout)

        if stderr is PIPE:
            self.stderr = Subprocess.__outputHandler(self.process.stderr)

    def __next__(self):
        return next(self.stdout)

    def __iter__(self):
        return self

    def __call__(self, inputSource):
        self.__setupInput(inputSource)
        return self

    def read(self):
        return self.process.stdout.read().decode("utf-8")

    def wait(self):
        return self.process.wait()

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


def devnull(iterable):
    for line in iterable:
        pass


def tee(iterable, n=2):
    it = iter(iterable)
    it_lock = threading.Lock()
    deques = [collections.deque() for i in range(n)]

    def gen(mydeque):
        while True:
            if not mydeque:  # when the local deque is empty
                if it_lock.acquire(False):  # and nobody waits
                    try:
                        newval = next(it)  # fetch a new value and
                        for d in deques:  # load it to all the deques
                            d.append(newval)
                    except StopIteration:
                        return
                    finally:
                        it_lock.release()
                else:  # if somebody already waits, wait for him
                    with it_lock:
                        pass
            else:
                yield mydeque.popleft()

    return tuple(gen(d) for d in deques)