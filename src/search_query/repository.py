import abc
from typing import List
from src.search_query.models import SearchQuery

from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, search_query: SearchQuery) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getByUserID(self, user_id: str) -> List[SearchQuery]:
        raise NotImplementedError

    @abc.abstractmethod
    def deleteByID(self, id: str) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, search_query: SearchQuery) -> None:
        query = self.session.query(SearchQuery).filter_by(text_query=search_query.text_query).first()
        if query:
            self.session.delete(query)
        self.session.add(search_query)
    
    def getByUserID(self, user_id: str) -> List[SearchQuery]:
        return self.session.query(SearchQuery).filter_by(owner_id=user_id).all()
    
    def deleteByID(self, id: str) -> None:
        search_query = self.session.query(SearchQuery).filter_by(id=id).first()
        self.session.delete(search_query)