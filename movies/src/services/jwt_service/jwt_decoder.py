import jwt
from core import config

def jwt_decoder(token: str) -> dict:
    decode_token = jwt.decode(jwt=token, key=config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
    return decode_token
