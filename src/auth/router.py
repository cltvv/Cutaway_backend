from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from src.auth.models import User
from src.auth.schemas import Token, UserRead, UserCreate, TokenData, UserUpdate
from src.auth.service import authenticate, create, update, get, CredentialsNotUnique
from src.auth.unit_of_work import SqlAlchemyUnitOfWork
from src.auth.utils import create_access_token, decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


auth_router = APIRouter()

user_router = APIRouter()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'msg': 'Could not validate credentials'},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_access_token(token)
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    current_user = get(SqlAlchemyUnitOfWork(), user_id)
    if not current_user:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={'msg': 'Token does not match any existing user'}
                )
    return current_user


@auth_router.post('/login', response_model=Token)
def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate(SqlAlchemyUnitOfWork(), form_data.username.lower(), form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': 'Incorrect username or password'},
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = create_access_token(user.id)
    return {
        'access_token': access_token,
        'token_type': 'Bearer'
    }


@auth_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserRead)
def register_user(user_in: UserCreate):
    try:
        registered_user = create(SqlAlchemyUnitOfWork(), user_in)
    except CredentialsNotUnique as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'loc': e.messages,
                'msg': 'A user with this email or username already exists'
            }
        )
    return registered_user


@user_router.get('/me', response_model=UserRead)
def get_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@user_router.patch('/me', response_model=UserRead)
def update_user(current_user: Annotated[User, Depends(get_current_user)], user_in: UserUpdate):
    try:
        updated_user = update(SqlAlchemyUnitOfWork(), current_user.id, user_in)
    except CredentialsNotUnique as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'loc': e.messages,
                'msg': 'A user with this email or username already exists'
            }
        )
    return updated_user
