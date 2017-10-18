envcontext
====

Context manager to update environment variables with preservation

[![Build status](https://img.shields.io/appveyor/ci/sakurai_youhei/envcontext/master.svg?label=Python%202.7%2C%203.3%20to%203.6%20%2F%20win32%20%26%20win_amd64)](https://ci.appveyor.com/project/sakurai_youhei/envcontext/branch/master)

- [envcontext on PyPI](https://pypi.python.org/pypi/envcontext)
- [envcontext on PyPI Test](https://testpypi.python.org/pypi/envcontext)

## Installation

```
pip install envcontext
```

## Usage

### Ex. 1: Update environment variables in current process

```python
from os import environ
from envcontext import EnvironmentContext as EnvContext

environ["TEST_VAR"] = "original"

with EnvContext(TEST_VAR="updated"):
    print(environ["TEST_VAR"])  # Prints "updated".

print(environ["TEST_VAR"])  # Prints "original".
```

### Ex. 2: Update environment variables in child process

```python
from subprocess import check_output
from envcontext import EnvironmentContext as EnvContext

with EnvContext(PGPASSWORD="very-secret-password"):
    check_output(["psql", "..."])  # psql process can manipulate PGPASSWORD.
```

_Note: Ex. 2 is not working on Python 2.x because subprocess module shipped with Python 2.x doesn't propagate environment variables from current to child process._
