from uuid import uuid4
from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.profile.schemas import ProfileCreate, ProfileRead
from src.search_query.schemas import SearchQueryString

from src.auth.router import get_current_user

from src.auth.models import User
from src.profile.models import Profile, Link

from src.auth.unit_of_work import SqlAlchemyUnitOfWork as SqlUserUow
from src.profile.unit_of_work import SqlAlchemyUnitOfWork as SqlProfileUow
from src.search_query.unit_of_work import SqlAlchemyUnitOfWork as SqlSearchQueryUow
from src.image.unit_of_work import SqlAlchemyUnitOfWork as SqlImageUow

from src.profile.service import create, get, delete, search_paginate, update
from src.image.service import get as get_image


profile_router = APIRouter()

user_profile_router = APIRouter()


# MARKER 7: this file contains endpoint definitions for the API consumer
# It's RESTful and it uses JSON

def get_current_user_profiles(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "User doesn't have any profiles"}
        )
    return current_user.profiles


def validate_images(image_uow: SqlImageUow, profile_picture_id: Optional[str], banner_picture_id: Optional[str]):
    loc = []
    if profile_picture_id:
        profile_picture_image = get_image(SqlImageUow(), profile_picture_id)
        if not profile_picture_image:
            loc.append('profile_picture')
    if banner_picture_id:
        banner_image = get_image(SqlImageUow(), banner_picture_id)
        if not banner_image:
            loc.append('banner')
    if loc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'loc': loc,
                    'msg': 'Image not found'}
        )


@user_profile_router.post('', status_code=status.HTTP_201_CREATED, response_model=ProfileRead)
def create_profile(new_profile: ProfileCreate, current_user: Annotated[User, Depends(get_current_user)]):
    profile = Profile(id=uuid4(), name=new_profile.name,
                      created_at=datetime.utcnow())
    profile_data = new_profile.dict(exclude={'links', 'name'})

    if new_profile.banner or new_profile.profile_picture:
        validate_images(
            SqlImageUow(), new_profile.profile_picture, new_profile.banner)

    for field in profile_data:
        setattr(profile, field, profile_data[field])
    if new_profile.links:
        for order, link in enumerate(new_profile.links):
            profile.links.add(Link(id=uuid4(),
                                   url=link.url,
                                   title=link.title,
                                   link_type=link.link_type,
                                   order=order))
    profile_response = ProfileRead.from_orm(profile)
    try:
        create(SqlUserUow(), current_user.id, profile)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': str(e)}
        )
    return profile_response


@user_profile_router.get('', response_model=List[ProfileRead])
def get_user_profiles(current_user_profiles: Annotated[User, Depends(get_current_user_profiles)]):
    profiles = sorted(current_user_profiles, key=lambda x: x.created_at)
    return profiles


@user_profile_router.get('/{profile_id}', response_model=ProfileRead)
def get_user_profile(current_user_profiles: Annotated[List[Profile], Depends(get_current_user_profiles)], profile_id: str):
    profile = next(
        (profile for profile in current_user_profiles if profile.id == profile_id), None)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "User doesn't have profile with this id"}
        )
    return profile


@user_profile_router.put('/{profile_id}', response_model=ProfileRead)
def update_user_profile(current_user_profiles: Annotated[List[Profile], Depends(get_current_user_profiles)], profile_id: str, new_profile: ProfileCreate):
    profile = [
        profile for profile in current_user_profiles if profile.id == profile_id]
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "User doesn't have profile with this id"}
        )

    if new_profile.banner or new_profile.profile_picture:
        validate_images(
            SqlImageUow(), new_profile.profile_picture, new_profile.banner)

    updated_profile = update(SqlProfileUow(), profile_id, new_profile)
    return updated_profile


@profile_router.get('/{profile_id}', response_model=ProfileRead)
def get_profile(profile_id: str):
    profile = get(SqlProfileUow(), profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': 'A profile with this id does not exist'}
        )
    return profile


@profile_router.get('/search/')
def search_profiles(current_user: Annotated[User, Depends(get_current_user)],
                    search_query: SearchQueryString = Depends(),
                    page: int = Query(1, ge=1),
                    size: int = Query(10, ge=1)
                    ):
    profiles, total = search_paginate(SqlProfileUow(),
                                      SqlSearchQueryUow(),
                                      SqlUserUow(),
                                      search_query.text_query,
                                      page, size,
                                      current_user.id)

    result = []
    for profile in profiles:
        result.append(ProfileRead.from_orm(profile))
    return {'total': total, 'items': result}


@user_profile_router.delete('/{profile_id}', status_code=204)
def delete_user_profile(current_user: Annotated[User, Depends(get_current_user)], profile_id: str):
    profile = [
        profile for profile in current_user.profiles if profile.id == profile_id]
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "User doesn't have profile with this id"}
        )
    delete(SqlProfileUow(), profile_id)
    return {}
