import abc

from src.profile.repository import AbstractRepository, SQLAlchemyRepository

from src.database import DEFAULT_SESSION_FACTORY


class AbstractUnitOfWork(abc.ABC):
    # MARKER 7: UoW pattern to safely modify data in the database
    # Allows to execute atomic operations, making it possible
    # to rollback if things go wrong

    profiles: AbstractRepository

    def __enter__(self):
        return self

    # MARKER 7: ends the database session when
    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    # MARKER 7: concrete implemenation of UoW interface

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        # MARKER 7: create database session implicitly
        # to make it easier to work with the database
        self.session = self.session_factory()
        self.profiles = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        # THIS WILL CRASH (most likely)
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        # MARKER 7: needs to be called explicitly
        self.session.commit()

    def rollback(self):
        # MARKER 7: will be called automatically
        self.session.rollback()
