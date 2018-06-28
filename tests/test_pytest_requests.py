# -*- coding: utf-8 -*-

import pytest


def test_fixture_simple_patch(testdir):
    """Most basic use case. Patch a simple """

    # create a temporary pytest test module
    testdir.makepyfile("""
        import requests

        def test_simple(requests_mock):
            with requests_mock.patch('/api/test') as patch:
                patch.returns = requests_mock.good('hello')
                response = requests.get('https://test.api/api/test')
                assert response.text == 'hello'
    """)

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_simple PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

@pytest.mark.xfail('Not implemented')
def test_help_message(testdir):
    result = testdir.runpytest(
        '--help',
    )
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'requests:',
        '*--foo=DEST_FOO*Set the value for the fixture "bar".',
    ])

@pytest.mark.xfail('Not implemented')
def test_hello_ini_setting(testdir):
    testdir.makeini("""
        [pytest]
        HELLO = world
    """)

    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def hello(request):
            return request.config.getini('HELLO')

        def test_hello_world(hello):
            assert hello == 'world'
    """)

    result = testdir.runpytest('-v')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_hello_world PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0
