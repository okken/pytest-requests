# -*- coding: utf-8 -*-

import pytest


def test_fixture_simple_patch(testdir):
    """Most basic use case. Patch a simple """

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import requests

        def test_simple(requests_mock):
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                response = requests.get('https://test.api/api/test')
                assert response.text == 'hello'
                assert patch.was_called_once()
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_fixture_simple_patch_with_session(testdir):
    """Use the patch with a requests session """

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import requests
        from requests.sessions import Session

        def test_simple_with_session(requests_mock):
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                with Session() as s:
                    response = s.get('https://test.api/api/test')
                    assert response.text == 'hello'
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_simple_with_session PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0


def test_fixture_simple_patch_with_session_raises_error(testdir):
    """Use the patch with a requests session """

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import requests
        from requests.sessions import Session
        import requests.exceptions
        import pytest

        def test_simple_with_session(requests_mock):
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.bad('hello')
                with Session() as s:
                    response = s.get('https://test.api/api/test')
                    assert response.text == 'hello'
                    with pytest.raises(requests.exceptions.HTTPError):
                        response.raise_for_status()
    """
    )
    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple_with_session PASSED*"])
    assert result.ret == 0


def test_fixture_json_api(testdir):
    """ Test a typical JSON API pattern"""

    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import requests
        import pytest

        def test_json(requests_mock):
            test_dict = {'a': 'b'}
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good(test_dict).as_json()
                response = requests.get('https://test.api/api/test')
                assert response.json() == test_dict
                assert 'Content-Type' in response.headers
                assert response.headers['Content-Type'] == 'application/json'
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_json PASSED*"])
    assert result.ret == 0


def test_fixture_bad_path(testdir):
    # create a temporary pytest test module
    testdir.makepyfile(
        """
        import requests
        import pytest

        def test_simple(requests_mock):
            with requests_mock.patch('/api/not_test') as patch:
                patch.returns = requests_mock.good('hello')
                with pytest.raises(AssertionError):
                    response = requests.get('https://test.api/api/test')
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])
    assert result.ret == 0


def test_mock_context(testdir):
    """Check that the patched HTTPAdapter is reset"""
    testdir.makepyfile(
        """
        import requests
        import requests.sessions
        import pytest

        def test_context(requests_mock):
            original = requests.sessions.HTTPAdapter
            with requests_mock.patch('/api/not_test') as patch:
                assert requests.sessions.HTTPAdapter is not original
            assert requests.sessions.HTTPAdapter is original
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_context PASSED*"])
    assert result.ret == 0


def test_returned_headers(testdir):
    testdir.makepyfile(
        """
        import requests
        import pytest

        def test_headers(requests_mock):
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello', headers={'X-Special': 'value'})
                response = requests.get('https://test.api/api/test')
                assert response.text == 'hello'
                assert response.headers['X-Special'] == 'value'
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_headers PASSED*"])
    assert result.ret == 0


def test_call_count(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_simple(requests_mock):
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                with pytest.raises(AssertionError):
                    assert patch.was_called_once()
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])
    assert result.ret == 0


def test_assert_headers(testdir):
    testdir.makepyfile(
        """
        import pytest
        import requests
        def test_simple(requests_mock):
            test_headers = {'X-Special': 'value'}
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                requests.get('https://api.com/api/test', headers=test_headers)
                assert patch.was_called_with_headers(test_headers)
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])
    assert result.ret == 0


def test_assert_headers_invalid(testdir):
    testdir.makepyfile(
        """
        import pytest
        import requests
        def test_simple(requests_mock):
            test_headers = {'X-Special': 'value'}
            test_headers_invalid = {'X-Special': 'not-value'}

            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                requests.get('https://api.com/api/test', headers=test_headers_invalid)
                with pytest.raises(AssertionError):
                    assert patch.was_called_with_headers(test_headers)
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])
    assert result.ret == 0


def test_assert_headers_casing(testdir):
    testdir.makepyfile(
        """
        import pytest
        import requests
        def test_simple(requests_mock):
            test_headers = {'X-Special': 'value'}
            test_headers_lower = {'x-special': 'value'}

            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                requests.get('https://api.com/api/test', headers=test_headers_lower)
                assert patch.was_called_with_headers(test_headers)
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])
    assert result.ret == 0


def test_assert_headers_ordering(testdir):
    testdir.makepyfile(
        """
        import pytest
        import requests

        def test_simple(requests_mock):
            test_headers = {'X-Special': 'value', 'X-Special-2': 'value2'}
            test_headers_2 = {'X-Special-2': 'value2', 'X-Special': 'value'}

            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                requests.get('https://api.com/api/test', headers=test_headers_2)
                assert patch.was_called_with_headers(test_headers)
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])
    assert result.ret == 0
