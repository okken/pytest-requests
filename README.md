# pytest-requests

[![PyPI version](https://img.shields.io/pypi/v/pytest-requests.svg)](https://pypi.org/project/pytest-requests) [![Python versions](https://img.shields.io/pypi/pyversions/pytest-requests.svg)](https://pypi.org/project/pytest-requests) [![See Build Status on Travis CI](https://travis-ci.org/okken/pytest-requests.svg?branch=master)](https://travis-ci.org/okken/pytest-requests) [![See Build Status on AppVeyor](https://ci.appveyor.com/api/projects/status/github/okken/pytest-requests?branch=master)](https://ci.appveyor.com/project/okken/pytest-requests/branch/master)

Fixtures to mock requests

------------------------------------------------------------------------

## Features

- Patch responses to APIs with static or dynamic data
- Support for both requests sessions and regular method calls
- Native support for setting responses as dicitonaries for JSON APIs

## Requirements

- PyTest 3.5+

## Installation

You can install \"pytest-requests\" via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

```bash
$ pip install pytest-requests
```

## Usage

In the most simple use case, just use the `requests_mock` fixture, which provides
a context manager called `patch`. It returns a patch instance which you can set the `.returns` value to a response. There is a response factory in `.good` or `.bad` which can take a string or a dictionary.

```python
import requests

def test_simple(requests_mock):
    with requests_mock.patch('/api/test') as patch:
        patch.returns = requests_mock.good('hello')
        response = requests.get('https://test.api/api/test')
        assert response.text == 'hello'
```

With sessions

```python
import requests
from requests.sessions import Session

def test_simple_with_session(requests_mock):
    with requests_mock.patch('/api/test') as patch:
        patch.returns = requests_mock.good('hello')
        with Session() as s:
            response = s.get('https://test.api/api/test')
            assert response.text == 'hello'
```

`requests_mock.good` or `requests_mock.bad` can also take a dictionary, which will be converted to a JSON string implicitly.

```python
import requests
import pytest

def test_json(requests_mock):
    test_dict = {'a': 'b'}
    with requests_mock.patch('/api/test') as patch:
        patch.returns = requests_mock.good(test_dict).as_json()
        response = requests.get('https://test.api/api/test')
        assert response.json() == test_dict
```

Returning specific headers.

```python
import requests
import pytest

def test_json(requests_mock):
    with requests_mock.patch('/api/test') as patch:
        patch.returns = requests_mock.good('hello', headers={'X-Special': 'value'})
        response = requests.get('https://test.api/api/test')
        assert response.text == 'hello'
        assert response.headers['X-Special'] == 'value'
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

## Credits

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated
with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[\@hackebrot](https://github.com/hackebrot)\'s
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
template.