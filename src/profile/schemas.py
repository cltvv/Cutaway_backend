import re
from datetime import datetime
from typing import Optional, List
from pydantic import EmailStr, AnyUrl, validator, conlist, UUID4, Field, constr

from src.profile.models import LinkType
from src.schemas import BaseModel


class LinkBase(BaseModel):
    url: AnyUrl
    title: str
    link_type: LinkType

    class Config:
        use_enum_values = True
        orm_mode = True


class ProfileCreate(BaseModel):
    name: constr(
        strip_whitespace=True,
        min_length=1,
        max_length=32)
    lastname: Optional[constr(strip_whitespace=True, min_length=1, max_length=32)]
    profile_picture: Optional[str]
    banner: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    place_of_work: Optional[constr(strip_whitespace=True, min_length=1, max_length=64)]
    education: Optional[constr(strip_whitespace=True, min_length=1, max_length=64)]
    links: Optional[conlist(LinkBase, max_items=10)]

    @validator('phone_number')
    def phone_validation(cls, phone_number):
        if not re.search(r"^(?:\+7\s)?\d{3}\s\d{3}-\d{2}-\d{2}$", phone_number):
            raise ValueError('Invalid phone number')
        return phone_number


class LinkResponse(LinkBase):
    order: Optional[int] = Field(exclude=True)


class ProfileRead(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    lastname: Optional[str]
    profile_picture: Optional[str]
    banner: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    place_of_work: Optional[str]
    education: Optional[str]
    links: Optional[conlist(LinkResponse, max_items=10)]

    @validator('links')
    def sort_links(cls, links):
        if links:
            return sorted(links, key=lambda x: x.order)
        return links
