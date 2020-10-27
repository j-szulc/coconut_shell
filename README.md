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
Work in progress - I'm going to upload the package to PyPI soon. Since the source is valid even in Python,
for now you can use it even without Coconut.