import os
import time
import uuid

from jwcrypto import jwk, jwt


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists.
    """
    return os.path.isfile(file_path)


def generate_keys(number_of_keys: int = 10, algorithm: str = "RS256", key_type: str = "RSA", key_size: int = 2048) -> jwk.JWKSet:
    """
    Generate a public/private key pair using EC algorithm.
    The key size is set to 2048 bits, and the algorithm is set to RSA-256.
    """
    keys: jwk.JWKSet = jwk.JWKSet()
    for i in range(number_of_keys):
        key: jwk.JWK = jwk.JWK.generate(kty=key_type, size=key_size, alg=algorithm, use="sig", kid=str(uuid.uuid4()))
        keys.add(key)
    return keys


def get_root_path() -> str:
    """
    Get the root path of the project.
    """
    return os.path.dirname(os.path.abspath(__file__))


def write_key_to_file(key, filename):
    """
    Write the provided key to a file.

    :param key: The key to write (public or private).
    :param filename: The name of the file to write the key to.
    """
    with open(os.path.join(get_root_path(), "files", filename), "w", encoding="utf-8") as file:
        file.write(key)


def read_keys_from_file(filename) -> jwk.JWKSet:
    """
    Read keys from a file.

    :param filename: The name of the file to read the key from.
    :return: The key read from the file.
    """
    with open(os.path.join(get_root_path(), "files", filename), "r", encoding="utf-8") as file:
        return jwk.JWKSet.from_json(file.read())


def parse_time_string(time_string: str) -> int:
    """
    Parse a time string into seconds.

    :param time_string: The time string to parse (e.g., "30m", "1h", "2d").
    :return: The parsed time in seconds.
    """
    if time_string.endswith("s"):
        return int(time_string[:-1])
    elif time_string.endswith("m"):
        return int(time_string[:-1]) * 60
    elif time_string.endswith("h"):
        return int(time_string[:-1]) * 3600
    elif time_string.endswith("d"):
        return int(time_string[:-1]) * 86400
    else:
        raise ValueError(f"Invalid time string: {time_string}")


def make_token(key: jwk.JWK, algorithm: str = "RS256", issuer: str = "", expiry="30m") -> str:
    """
    Create a JWT token using the provided key.

    :param key: The key to use for signing the token.
    :return: The signed JWT token.
    """
    if not issuer:
        raise ValueError("Issuer is required")
    token = jwt.JWT(
        header={
            "alg": algorithm,
            "typ": key.get("typ"),
            "kid": key.get("kid"),
        },
        claims={
            "iss": issuer,
            "sub": "thetoken",
            "aud": "api://AzureADTokenExchange",
            "exp": int(time.time() + parse_time_string(expiry)),
            "iat": int(time.time()),
            "nbf": int(time.time()),
            "jti": str(uuid.uuid4()),
        },
    )
    token.make_signed_token(jwk.JWK(**key))
    return token.serialize(compact=True)


def first_time_setup(force: bool = False, **kwargs) -> None:
    """
    Perform first time setup.
    """
    if (not file_exists("jwks_private") and not file_exists("jwks")) or force:
        keys = generate_keys(**kwargs)
        write_key_to_file(keys.export(private_keys=False), "jwks")
        write_key_to_file(keys.export(private_keys=True), "jwks_private")
