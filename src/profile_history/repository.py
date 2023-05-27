import abc
from typing import Set, List
from src.profile_history.models import HistoryProfile
from src.profile.models import Profile

from sqlalchemy.orm.session import Session
from sqlalchemy.orm import subqueryload, joinedload


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, profile: HistoryProfile) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getByID(self, id: str) -> HistoryProfile:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getByUserID(self, user_id: str) -> List[HistoryProfile]:
        raise NotImplementedError

    @abc.abstractmethod
    def deleteByProfileID(self, profile_id: str) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, bookmark: HistoryProfile) -> None:
        self.session.add(bookmark)
    
    def getByID(self, id: str) -> HistoryProfile:
        return self.session.query(HistoryProfile).options(joinedload(HistoryProfile.profile).subqueryload(Profile.links)).filter_by(id=id).one_or_none()
    
    def getByUserID(self, user_id: str) -> List[HistoryProfile]:
        return self.session.query(HistoryProfile).options(joinedload(HistoryProfile.profile).subqueryload(Profile.links)).filter_by(owner_id=user_id).all()

    def deleteByProfileID(self, profile_id: str) -> None:
        bookmark = self.session.query(HistoryProfile).filter_by(profile_id=profile_id).first()
        self.session.delete(bookmark)