import os


def get_env_bool(name: str) -> bool:
    """
    Get an environment variable as a boolean.
    """
    return os.getenv(name, "false").lower() in ("true", "1", "t")


def get_env_string(name: str) -> str:
    """
    Get an environment variable as a string.
    """
    return os.getenv(name, "")


def get_env_int(name: str) -> int:
    """
    Get an environment variable as an integer.
    """
    return int(os.getenv(name, 0))


def get_env_float(name: str) -> float:
    """
    Get an environment variable as a float.
    """
    return float(os.getenv(name, 0.0))


def get_env_list(name: str) -> list:
    """
    Get an environment variable as a list.
    """
    return os.getenv(name, "").split(",")


def get_env_dict(name: str) -> dict:
    """
    Get an environment variable as a dictionary.
    """
    if not os.getenv(name):
        return {}
    return dict(item.split("=") for item in os.getenv(name, "").split(","))


def get_env_json(name: str) -> dict:
    """
    Get an environment variable as a JSON object.
    """
    import json

    return json.loads(os.getenv(name, "{}"))


def get_env_tuple(name: str) -> tuple:
    """
    Get an environment variable as a tuple.
    """
    return tuple(os.getenv(name, "").split(","))


def get_env_set(name: str) -> set:
    """
    Get an environment variable as a set.
    """
    return set(os.getenv(name, "").split(","))


def get_env_path(name: str) -> str:
    """
    Get an environment variable as a file path.
    """
    return os.path.abspath(os.getenv(name, ""))
