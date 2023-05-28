from uuid import uuid4
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import subqueryload
from sqlalchemy import text, func, and_, or_
from fastapi import HTTPException, status

from src.auth.unit_of_work import AbstractUnitOfWork as UserUow
from src.profile.unit_of_work import AbstractUnitOfWork as ProfileUow
from src.search_query.unit_of_work import AbstractUnitOfWork as SearchQueryUow
from src.image.unit_of_work import AbstractUnitOfWork as ImageUow

from src.profile.models import Profile, Link
from src.search_query.models import SearchQuery

from src.profile.schemas import ProfileCreate


# MARKER 6: uses domain level class and UoW pattern
# to store data in the database
def create(uow: UserUow, user_id: str, profile: Profile) -> None:
    with uow:
        user = uow.users.getByID(user_id)
        user.add_profile(profile)
        uow.commit()


def get(uow: ProfileUow, profile_id: str) -> Profile:
    with uow:
        profile = uow.profiles.getByID(profile_id)
        uow.commit()
    return profile


def delete(uow: ProfileUow, profile_id: str) -> None:
    with uow:
        uow.profiles.deleteByID(profile_id)
        uow.commit()


def update(uow: ProfileUow, profile_id: str, new_profile: ProfileCreate) -> Profile:
    with uow:
        profile = uow.profiles.getByID(profile_id)
        profile_data = new_profile.dict(exclude={'links'})
        for field in profile_data:
            setattr(profile, field, profile_data[field])
        if new_profile.links:
            profile.links.clear()
            for order, link in enumerate(new_profile.links):
                profile.links.add(Link(id=uuid4(),
                                       url=link.url,
                                       title=link.title,
                                       link_type=link.link_type,
                                       order=order))
        if new_profile.links == []:
            profile.links.clear()
        uow.commit()
    return profile


def search_paginate(profile_uow: ProfileUow,
                    search_query_uow: SearchQueryUow,
                    user_uow: UserUow,
                    text_query: str,
                    page: int,
                    size: int,
                    user_id: str):
    with profile_uow:
        query = (
            profile_uow.session.query(Profile)
            .options(subqueryload(Profile.links))
        )
        query = query.filter(and_(
            or_(
                text("LOWER(name) LIKE LOWER(:text_query)"),
                text("LOWER(lastname) LIKE LOWER(:text_query)"),
                text("LOWER(name || ' ' || lastname) LIKE LOWER(:text_query)")
            ),
            text("owner_id != :user_id")
        )).params(text_query=f"%{text_query}%", user_id=f"{user_id}")
        total_count = query.count()
        profiles = (
            query
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        profile_uow.commit()

    with user_uow:
        user = user_uow.users.getByID(user_id)
        user_uow.commit()

    with search_query_uow:
        search_query_uow.search_queries.add(SearchQuery(
            uuid4(), user, text_query, created_at=datetime.utcnow()))
        search_query_uow.commit()

    return profiles, total_count
