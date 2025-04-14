import os

import pytest

from src.helpers import (
    get_env_bool,
    get_env_dict,
    get_env_float,
    get_env_int,
    get_env_json,
    get_env_list,
    get_env_path,
    get_env_set,
    get_env_string,
    get_env_tuple,
)


@pytest.fixture(autouse=True)
def clear_env():
    """
    Clear environment variables before each test.
    """
    os.environ.clear()


def test_get_env_bool():
    os.environ["TEST_BOOL"] = "true"
    assert get_env_bool("TEST_BOOL") is True

    os.environ["TEST_BOOL"] = "false"
    assert get_env_bool("TEST_BOOL") is False

    os.environ["TEST_BOOL"] = "1"
    assert get_env_bool("TEST_BOOL") is True

    os.environ["TEST_BOOL"] = "0"
    assert get_env_bool("TEST_BOOL") is False


def test_get_env_string():
    os.environ["TEST_STRING"] = "hello"
    assert get_env_string("TEST_STRING") == "hello"

    assert get_env_string("NON_EXISTENT") == ""


def test_get_env_int():
    os.environ["TEST_INT"] = "42"
    assert get_env_int("TEST_INT") == 42

    assert get_env_int("NON_EXISTENT") == 0


def test_get_env_float():
    os.environ["TEST_FLOAT"] = "3.14"
    assert get_env_float("TEST_FLOAT") == 3.14

    assert get_env_float("NON_EXISTENT") == 0.0


def test_get_env_list():
    os.environ["TEST_LIST"] = "a,b,c"
    assert get_env_list("TEST_LIST") == ["a", "b", "c"]

    assert get_env_list("NON_EXISTENT") == [""]


def test_get_env_dict():
    os.environ["TEST_DICT"] = "key1=value1,key2=value2"
    assert get_env_dict("TEST_DICT") == {"key1": "value1", "key2": "value2"}

    assert get_env_dict("NON_EXISTENT") == {}


def test_get_env_json():
    os.environ["TEST_JSON"] = '{"key": "value"}'
    assert get_env_json("TEST_JSON") == {"key": "value"}

    assert get_env_json("NON_EXISTENT") == {}


def test_get_env_tuple():
    os.environ["TEST_TUPLE"] = "a,b,c"
    assert get_env_tuple("TEST_TUPLE") == ("a", "b", "c")

    assert get_env_tuple("NON_EXISTENT") == ("",)


def test_get_env_set():
    os.environ["TEST_SET"] = "a,b,c"
    assert get_env_set("TEST_SET") == {"a", "b", "c"}

    assert get_env_set("NON_EXISTENT") == {""}


def test_get_env_path():
    os.environ["TEST_PATH"] = "/tmp/test"
    assert get_env_path("TEST_PATH") == os.path.abspath("/tmp/test")

    assert get_env_path("NON_EXISTENT") == os.path.abspath("")
