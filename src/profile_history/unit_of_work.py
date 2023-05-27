import abc

from src.profile_history.repository import AbstractRepository, SQLAlchemyRepository

from src.database import DEFAULT_SESSION_FACTORY


class AbstractUnitOfWork(abc.ABC):

    history_profiles: AbstractRepository

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.rollback()
    
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
    

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session = self.session_factory()
        self.history_profiles = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()