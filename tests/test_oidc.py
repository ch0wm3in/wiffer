import os
from unittest.mock import mock_open, patch

import pytest
from jwcrypto import jwk

from src.oidc import (
    file_exists,
    first_time_setup,
    generate_keys,
    get_root_path,
    make_token,
    parse_time_string,
    read_keys_from_file,
    write_key_to_file,
)


def test_parse_time_string_seconds():
    assert parse_time_string("30s") == 30
    assert parse_time_string("0s") == 0


def test_parse_time_string_minutes():
    assert parse_time_string("1m") == 60
    assert parse_time_string("15m") == 900


def test_parse_time_string_hours():
    assert parse_time_string("1h") == 3600
    assert parse_time_string("2h") == 7200


def test_parse_time_string_days():
    assert parse_time_string("1d") == 86400
    assert parse_time_string("2d") == 172800


def test_parse_time_string_invalid_format():
    with pytest.raises(ValueError, match="Invalid time string: 30x"):
        parse_time_string("30x")
    with pytest.raises(ValueError, match="Invalid time string: 1"):
        parse_time_string("1")
    with pytest.raises(ValueError, match="Invalid time string: "):
        parse_time_string("")


def test_file_exists(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("content")
    assert file_exists(str(test_file)) is True
    assert file_exists(str(tmp_path / "nonexistent.txt")) is False


def test_generate_keys():
    keys = generate_keys(number_of_keys=2)
    assert len(keys["keys"]) == 2
    for key in keys:
        assert isinstance(key, jwk.JWK)


def test_get_root_path():
    assert os.path.basename(get_root_path()) == "src"


@patch("builtins.open", new_callable=mock_open)
@patch("src.oidc.get_root_path", return_value="/mocked/path")
def test_write_key_to_file(mock_get_root_path, mock_open_file):
    write_key_to_file("mocked_key", "mocked_file")
    mock_open_file.assert_called_once_with("/mocked/path/files/mocked_file", "w", encoding="utf-8")
    mock_open_file().write.assert_called_once_with("mocked_key")


@patch("builtins.open", new_callable=mock_open, read_data='{"keys": []}')
@patch("src.oidc.get_root_path", return_value="/mocked/path")
def test_read_keys_from_file(mock_get_root_path, mock_open_file):
    keys = read_keys_from_file("mocked_file")
    assert isinstance(keys, jwk.JWKSet)
    mock_open_file.assert_called_once_with("/mocked/path/files/mocked_file", "r", encoding="utf-8")


@patch("src.oidc.time.time", return_value=1000000)
@patch("src.oidc.parse_time_string", return_value=1800)
def test_make_token(mock_parse_time_string, mock_time):
    key = jwk.JWK.generate(kty="RSA", size=2048)
    token = make_token(key, issuer="test_issuer", expiry="30m")
    assert isinstance(token, str)
    assert "eyJ" in token  # Basic check for JWT format


@patch("src.oidc.file_exists", return_value=False)
@patch("src.oidc.write_key_to_file")
@patch("src.oidc.generate_keys")
def test_first_time_setup(mock_generate_keys, mock_write_key_to_file, mock_file_exists):
    mock_keys = jwk.JWKSet()
    mock_generate_keys.return_value = mock_keys
    first_time_setup()
    mock_generate_keys.assert_called_once()
    mock_write_key_to_file.assert_any_call(mock_keys.export(private_keys=False), "jwks")
    mock_write_key_to_file.assert_any_call(mock_keys.export(private_keys=True), "jwks_private")
