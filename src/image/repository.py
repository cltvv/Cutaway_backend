import abc
from src.image.models import Image

from sqlalchemy.orm.session import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, image: Image) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getByID(self, id: str) -> Image:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, image: Image) -> None:
        self.session.add(image)
    
    def getByID(self, id: str) -> Image:
        return self.session.query(Image).filter_by(id=id).one_or_none()
    