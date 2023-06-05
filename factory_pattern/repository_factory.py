from src.auth.repository import XPathRepository, JSONRepository


class UserRepositoryFactory:
    @staticmethod
    def get_repository(format: str) -> object:
        if format == 'JSON':
            return JSONRepository('users.json')
        if format == 'XML':
            return XPathRepository('users.xml')
        raise ValueError(format)
