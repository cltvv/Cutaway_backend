from dataclasses import dataclass
from src.profile.models import Profile
from src.auth.models import User
from datetime import datetime


@dataclass
class HistoryProfile():
    def __init__(self, 
                 id: str,
                 user: User,
                 profile: Profile,
                 created_at: datetime):
        self.id = id
        self.owner = user
        self.profile = profile
        self.created_at = created_at