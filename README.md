# pytest-requests

[![PyPI version](https://img.shields.io/pypi/v/pytest-requests.svg)](https://pypi.org/project/pytest-requests) [![Python versions](https://img.shields.io/pypi/pyversions/pytest-requests.svg)](https://pypi.org/project/pytest-requests) [![See Build Status on Travis CI](https://travis-ci.org/okken/pytest-requests.svg?branch=master)](https://travis-ci.org/okken/pytest-requests) [![See Build Status on AppVeyor](https://ci.appveyor.com/api/projects/status/github/okken/pytest-requests?branch=master)](https://ci.appveyor.com/project/okken/pytest-requests/branch/master)

Fixtures to mock requests

------------------------------------------------------------------------

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated
with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[\@hackebrot](https://github.com/hackebrot)\'s
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
template.

## Features

-   TODO

## Requirements

-   TODO

## Installation

You can install \"pytest-requests\" via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

```bash
$ pip install pytest-requests
```

## Usage

In the most simple use case, just use the `requests_mock` fixture, which provides
a context manager called `patch`. It returns a patch instance which you can set the `.returns` value to a response. There is a response factory in `.good` or `.bad` which can take a string.

```python
import requests

def test_simple(requests_mock):
    with requests_mock.patch('/api/test') as patch:
        patch.returns = requests_mock.good('hello')
        response = requests.get('https://test.api/api/test')
        assert response.text == 'hello'
```

## Contributing

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage
at least stays the same before you submit a pull request.

## License

Distributed under the terms of the
[MIT](http://opensource.org/licenses/MIT) license, \"pytest-requests\"
is free and open source software

## Issues

If you encounter any problems, please [file an
issue](https://github.com/okken/pytest-requests/issues) along with a
detailed description.
