import abc
from typing import Set
from src.auth.models import User
from src.profile.models import Profile
from src.bookmark.models import Bookmark

from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload, subqueryload

import datetime
import lxml.etree as etree


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def getByID(self, id: str) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getByUsername(self, username: str) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def getByEmail(self, email: str) -> User:
        raise NotImplementedError


class FakeRepository(AbstractRepository):

    def __init__(self, users: Set[User] = set()):
        self._users = users

    def add(self, user: User) -> None:
        self._users.add(user)

    def getByID(self, id: str):
        return next(u for u in self._users if u.id == id)
    
    def getByUsername(self, username: str):
        return next(u for u in self._users if u.username == username)
    
    def getByEmail(self, email: str):
        return next(u for u in self._users if u.email == email)


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    def getByID(self, id: str) -> User:
        query = self.session.query(User)
        query = query.options(
            joinedload(User.profiles).subqueryload(Profile.links),
        )
        user = query.filter_by(id=id).one_or_none()
        return user
    
    def getByUsername(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).one_or_none()
    
    def getByEmail(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).one_or_none()
    

class XPathRepository(AbstractRepository):
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.tree = etree.parse(xml_file_path)

    def add(self, user):
        root = self.tree.getroot()

        new_user_element = etree.Element("user")
        new_user_element.set("id", user.id)

        username_element = etree.Element("username")
        username_element.text = user.username
        new_user_element.append(username_element)

        email_element = etree.Element("email")
        email_element.text = user.email
        new_user_element.append(email_element)

        hashed_password_element = etree.Element("hashed_password")
        hashed_password_element.text = user.hashed_password
        new_user_element.append(hashed_password_element)

        is_active_element = etree.Element("is_active")
        is_active_element.text = str(user.is_active)
        new_user_element.append(is_active_element)

        created_at_element = etree.Element("created_at")
        created_at_element.text = user.created_at.isoformat()
        new_user_element.append(created_at_element)

        root.append(new_user_element)
        self.tree.write(self.xml_file_path, pretty_print=True)

    def getByID(self, id):
        user_elements = self.tree.xpath(f"//user[@id='{id}']")
        if user_elements:
            return self._parse_user_element(user_elements[0])
        return None

    def getByUsername(self, username):
        user_elements = self.tree.xpath(f"//user[username='{username}']")
        if user_elements:
            return self._parse_user_element(user_elements[0])
        return None

    def getByEmail(self, email):
        user_elements = self.tree.xpath(f"//user[email='{email}']")
        if user_elements:
            return self._parse_user_element(user_elements[0])
        return None

    def _parse_user_element(self, user_element):
        id = user_element.get("id")
        username = user_element.xpath("username")[0].text
        email = user_element.xpath("email")[0].text
        hashed_password = user_element.xpath("hashed_password")[0].text
        is_active = user_element.xpath("is_active")[0].text.lower() == "true"
        created_at = user_element.xpath("created_at")[0].text

        return User(id, username, email, hashed_password, is_active, created_at)



