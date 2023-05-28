import abc
from typing import Set, List
from src.profile.models import Profile

from sqlalchemy.orm.session import Session
from sqlalchemy.orm import subqueryload, joinedload


class AbstractRepository(abc.ABC):
    # MARKER 3: repository interface
    # to allow for multiple implementations

    @abc.abstractmethod
    def add(self, profile: Profile) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def getByID(self, id: str) -> Profile:
        raise NotImplementedError

    @abc.abstractmethod
    def deleteByID(self, id: str) -> None:
        raise NotImplementedError


class FakeRepository(AbstractRepository):
    # MARKER 3: fake repo implementation
    # storing data in memory

    def __init__(self, profiles: Set[Profile] = set()):
        self._profiles = profiles

    def add(self, profile: Profile) -> None:
        self._profiles.add(profile)

    def getByID(self, id: str) -> Profile:
        return next(p for p in self._profiles if p.id == id)


class SQLAlchemyRepository(AbstractRepository):
    # MARKER 5: real repo implementation
    # interacting with SqlAlchemy

    def __init__(self, session: Session):
        self.session = session

    def add(self, profile: Profile) -> None:
        self.session.add(profile)

    def getByID(self, id: str) -> Profile:
        return self.session.query(Profile).options(joinedload(Profile.links)).filter_by(id=id).one_or_none()

    def deleteByID(self, id: str) -> None:
        profile = self.session.query(Profile).filter_by(id=id).first()
        self.session.delete(profile)
