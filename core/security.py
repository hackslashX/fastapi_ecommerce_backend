import jwt
from datetime import datetime, timedelta
from passlib.hash import argon2


from instance.config import config


def get_password_hash(password: str) -> str:
    return argon2.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return argon2.verify(plain_password, hashed_password)


def create_jwt_token(payload: dict, typ: str = "access") -> str:
    if typ == "refresh":
        expire_delta = config.JWT_CONFIG.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    else:
        expire_delta = config.JWT_CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_delta)
    to_encode = {"exp": expire, "typ": typ, **payload}
    encoded_jwt = jwt.encode(
        to_encode,
        config.JWT_CONFIG.JWT_SECRET_KEY,
        algorithm=config.JWT_CONFIG.JWT_ALGORITHM,
    )
    return encoded_jwt
