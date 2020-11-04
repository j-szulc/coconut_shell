# coconut-shell
Bash bindings so I don't have to code in bash ever again.

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
