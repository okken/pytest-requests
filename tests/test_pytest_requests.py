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

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_simple_with_session PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
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
    """
    )

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_json PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
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

    # run pytest with the following cmd args
    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(["*::test_simple PASSED*"])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0