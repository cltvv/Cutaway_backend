from uuid import uuid4
from datetime import datetime
from typing import Optional, List

from src.auth.models import User
from src.auth.schemas import UserUpdate, UserCreate
from src.auth.unit_of_work import AbstractUnitOfWork
from src.auth.utils import verify_password, get_password_hash


class CredentialsNotUnique(Exception):
    def __init__(self, messages: List[str]):
        self.messages = messages
        super().__init__("Credentials not unique")


def authenticate(uow: AbstractUnitOfWork, username: str, password: str) -> User:
    with uow:
        user = uow.users.getByUsername(username)
        uow.commit()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def credentials_unique(uow: AbstractUnitOfWork, email: str, username: str, user_id: Optional[str] | None = None):
    with uow:
        loc = []
        user_from_username = uow.users.getByUsername(username)
        user_from_email = uow.users.getByEmail(email)
        if user_from_username:
            if user_from_username.id != user_id:
                loc.append('username')
        if user_from_email:
            if user_from_email.id != user_id:
                loc.append('email')
        if loc:
            raise CredentialsNotUnique(loc)
    return True

def create(uow: AbstractUnitOfWork, user_in: UserCreate) -> User:
    if credentials_unique(uow, user_in.email, user_in.username):
        user = User(str(uuid4()),
                    user_in.username,
                    user_in.email,
                    get_password_hash(user_in.password),
                    created_at=datetime.utcnow())
        with uow:
            uow.users.add(user)
            uow.commit()
        return user
    


def get(uow: AbstractUnitOfWork, id: str) -> User:
    with uow:
        user = uow.users.getByID(id)
        uow.commit()
    return user


def update(uow: AbstractUnitOfWork, user_id: str, user_in: UserUpdate) -> User:
    if credentials_unique(uow, user_in.email, user_in.username, user_id):
        with uow:
            user = uow.users.getByID(user_id)
            update_data = user_in.dict(exclude={'password'})
            for field in update_data:
                if update_data[field]:
                    setattr(user, field, update_data[field])
            if user_in.password:
                user.hashed_password = get_password_hash(user_in.password)
            uow.commit()
    return user
