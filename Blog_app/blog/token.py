import jwt
from . import schemas
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from .models import User
from .database import get_db

#  A random secret key that will be used to sign the JWT tokens.
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d5g7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credetials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credetials_exception
        token_data =  schemas.TokenData(email=email)
    except InvalidTokenError:
        raise credetials_exception

# We can move the routes behind this token based authentication to secure from unauthorized access.