from dataclasses import dataclass
from datetime import datetime
from src.auth.models import User


@dataclass(unsafe_hash=True)
class SearchQuery():
    def __init__(self, 
                 id: str,
                 user: User,
                 text_query: str,
                 created_at: datetime):
        self.id = id 
        self.owner = user
        self.text_query = text_query
        self.created_at = created_at
