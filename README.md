<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/coconut_shell.svg?branch=main)](https://cirrus-ci.com/github/<USER>/coconut_shell)
[![ReadTheDocs](https://readthedocs.org/projects/coconut_shell/badge/?version=latest)](https://coconut_shell.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/coconut_shell/main.svg)](https://coveralls.io/r/<USER>/coconut_shell)
[![PyPI-Server](https://img.shields.io/pypi/v/coconut_shell.svg)](https://pypi.org/project/coconut_shell/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/coconut_shell.svg)](https://anaconda.org/conda-forge/coconut_shell)
[![Monthly Downloads](https://pepy.tech/badge/coconut_shell/month)](https://pepy.tech/project/coconut_shell)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/coconut_shell)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# coconut_shell

Bash bindings for python / coconut, so that I don't have to code in bash ever again

## Coconut ⊃ Python
[Coconut](http://coconut-lang.org/) is a Python superset (any valid Python code is a valid Coconut code), which compiles to Python.
It adds various functional programming features like:
* pretty lambdas
```python
x -> x ** 2
``` 

* pretty definitions for partial functions
```python
pow$(?,2)
(**) 2
```

* but most importantly: pipes!
```python
"hello, world!" |> print
```

## Examples
This library provides you with the only good thing about bash - shell pipes, but in Coconut!
For example, you could do something like this:
```python
sh("ls") |> filter$(.endswith(".py")) |> sh("tail -n1") |> cat
```
or like this
```python
from itertools import count
sh("ping 8.8.8.8") |> zip$(count()) |> cat
```

## Installation
Even though this library is meant to be used in the Coconut language, I will maintain this repository as a valid Python 3 code so that it can also be used this way directly in Python.

I will upload the library to the PyPI soon.