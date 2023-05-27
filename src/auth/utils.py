from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from src.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_AUTH, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password, pwd_context: CryptContext = pwd_context) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str,  pwd_context: CryptContext = pwd_context) -> str:
    return pwd_context.hash(password)

def create_access_token(user_id: str) -> str:
    to_encode = {
        'sub': user_id
    }
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_AUTH, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_AUTH, algorithms=[ALGORITHM])
    value = payload.get('sub')
    return value
