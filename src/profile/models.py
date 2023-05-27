from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set, List
from datetime import datetime


class LinkType(Enum):
    FACEBOOK = 'facebook'
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'
    LINKEDIN = 'linkedin'
    YOUTUBE = 'youTube'
    TIKTOK = 'tiktok'
    PINTEREST = 'pinterest'
    CUSTOM = 'custom'


@dataclass(unsafe_hash=True)
class Link():
    id: str
    url: str
    title: str
    link_type: LinkType
    order: int


class Profile:
    def __init__(self, 
                 id: str,
                 name: str,
                 created_at: datetime,
                 lastname: Optional[str] | None = None,
                 profile_picture: Optional[str] | None = None,
                 banner: Optional[str] | None = None,
                 phone_number: Optional[str] | None = None,
                 email: Optional[str] | None = None,
                 place_of_work: Optional[str] | None = None,
                 education: Optional[str] | None = None,
                 links: Set[Link] = set()):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.profile_picture = profile_picture
        self.banner = banner
        self.phone_number = phone_number
        self.email = email
        self.place_of_work = place_of_work
        self.education = education
        self.created_at = created_at
        self._links = links
    
    @property
    def links(self) -> Optional[Set[Link]]:
        return sorted(self._links, key=lambda link: link.order)
    
    @links.setter
    def links(self, value: Set[Link]):
        self._links = sorted(value, key=lambda link: link.order)

    def __eq__(self, other):
        if not isinstance(other, Profile):
            return False
        return other.id == self.id
    
    def __hash__(self):
        return hash(self.id)