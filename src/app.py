import random

from flask import Flask, jsonify

from src.helpers import get_env_bool, get_env_int, get_env_string
from src.oidc import first_time_setup, make_token, read_keys_from_file


def create_app():
    app = Flask(__name__)

    # Load environment variables
    app.config["REGEN_KEYS_AT_RESTART"] = get_env_bool("REGEN_KEYS_AT_RESTART") or True
    app.config["JWKS_URI"] = get_env_string("JWKS_URI") or "http://localhost/.well-known/jwks"
    app.config["KEY_ALGORITHM"] = get_env_string("KEY_ALGORITHM") or "RS256"
    app.config["ISSUER"] = get_env_string("ISSUER") or "http://localhost"
    app.config["KEY_TYPE"] = get_env_string("KEY_TYPE") or "RSA"
    app.config["NUMBER_OF_KEYS"] = get_env_int("NUMBER_OF_KEYS") or 10
    app.config["KEY_SIZE"] = get_env_int("KEY_SIZE") or 2048
    app.config["TOKEN_EXPIRATION_TIME"] = get_env_string("TOKEN_EXPIRATION_TIME") or "30m"

    first_time_setup(
        force=app.config["REGEN_KEYS_AT_RESTART"],
        number_of_keys=app.config["NUMBER_OF_KEYS"],
        key_type=app.config["KEY_TYPE"],
        key_size=app.config["KEY_SIZE"],
        algorithm=app.config["KEY_ALGORITHM"],
    )

    # Load keys into memeory
    app.config["JWKS_PUBLIC"] = read_keys_from_file("jwks").export(as_dict=True)
    app.config["JWKS_PRIVATE"] = read_keys_from_file("jwks_private").export(private_keys=True, as_dict=True)

    return app


app = create_app()


@app.route("/.well-known/jwks", methods=["GET"])
def get_jwks():
    """
    Endpoint to retrieve the JSON Web Key Set (JWKS).
    """

    # Return the JWKS as JSON
    return jsonify(app.config["JWKS_PUBLIC"]), 200


@app.route("/.well-known/openid-configuration", methods=["GET"])
def get_open_id_configuration():
    """
    Endpoint to retrieve the OpenID configuration.
    """
    return (
        jsonify(
            {
                "issuer": app.config["ISSUER"],
                "jwks_uri": app.config["JWKS_URI"],
                "response_types_supported": ["code", "id_token", "id_token code"],
                "subject_types_supported": ["public"],
                "id_token_signing_alg_values_supported": [app.config["KEY_ALGORITHM"] or "RS256"],
                "scopes_supported": ["openid", "profile", "email"],
                "token_endpoint_auth_methods_supported": ["client_secret_basic"],
            }
        ),
        200,
    )


@app.route("/token", methods=["GET"])
def get_token():
    """
    Endpoint to retrieve a token.
    """
    random_key = app.config["JWKS_PRIVATE"]["keys"][random.randint(0, len(app.config["JWKS_PRIVATE"]["keys"])) - 1]  # nosec: B311
    token = make_token(
        random_key, algorithm=app.config["KEY_ALGORITHM"], issuer=app.config["ISSUER"], expiry=app.config["TOKEN_EXPIRATION_TIME"]
    )
    return jsonify({"token": token}), 200
