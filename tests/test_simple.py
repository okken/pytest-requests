# -*- coding: utf-8 -*-

import pytest
import requests
from requests.sessions import Session
import requests.sessions
import requests.exceptions


def test_fixture_simple_patch(requests_mock):
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        response = requests.get("https://test.api/api/test")
        assert response.text == "hello"
        assert patch.was_called_once()


def test_fixture_simple_patch_with_session(requests_mock):
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        with Session() as s:
            response = s.get("https://test.api/api/test")
            assert response.text == "hello"


def test_fixture_simple_patch_with_session_raises_error(requests_mock):
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.bad("hello")
        with Session() as s:
            response = s.get("https://test.api/api/test")
            assert response.text == "hello"
            with pytest.raises(requests.exceptions.HTTPError):
                response.raise_for_status()


def test_fixture_json_api(requests_mock):
    test_dict = {"a": "b"}
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good(test_dict).as_json()
        response = requests.get("https://test.api/api/test")
        assert response.json() == test_dict
        assert "Content-Type" in response.headers
        assert response.headers["Content-Type"] == "application/json"


def test_fixture_bad_path(requests_mock):
    with requests_mock.patch("/api/not_test") as patch:
        patch.returns = requests_mock.good("hello")
        with pytest.raises(AssertionError):
            requests.get("https://test.api/api/test")


def test_mock_context(requests_mock):
    original = requests.sessions.HTTPAdapter
    with requests_mock.patch("/api/not_test"):
        assert requests.sessions.HTTPAdapter is not original
    assert requests.sessions.HTTPAdapter is original


def test_returned_headers(requests_mock):
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello", headers={"X-Special": "value"})
        response = requests.get("https://test.api/api/test")
        assert response.text == "hello"
        assert response.headers["X-Special"] == "value"


def test_call_count(requests_mock):
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        with pytest.raises(AssertionError):
            assert patch.was_called_once()


def test_assert_headers(requests_mock):
    test_headers = {"X-Special": "value"}
    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        requests.get("https://api.com/api/test", headers=test_headers)
        assert patch.was_called_with_headers(test_headers)


def test_assert_headers_invalid(requests_mock):
    test_headers = {"X-Special": "value"}
    test_headers_invalid = {"X-Special": "not-value"}

    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        requests.get("https://api.com/api/test", headers=test_headers_invalid)
        with pytest.raises(AssertionError):
            assert patch.was_called_with_headers(test_headers)


def test_assert_headers_casing(requests_mock):
    test_headers = {"X-Special": "value"}
    test_headers_lower = {"x-special": "value"}

    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        requests.get("https://api.com/api/test", headers=test_headers_lower)
        assert patch.was_called_with_headers(test_headers)


def test_assert_headers_ordering(requests_mock):
    test_headers = {"X-Special": "value", "X-Special-2": "value2"}
    test_headers_2 = {"X-Special-2": "value2", "X-Special": "value"}

    with requests_mock.patch("/api/test") as patch:
        patch.returns = requests_mock.good("hello")
        requests.get("https://api.com/api/test", headers=test_headers_2)
        assert patch.was_called_with_headers(test_headers)
