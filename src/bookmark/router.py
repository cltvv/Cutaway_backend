from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Annotated, List

from src.auth.models import User
from src.auth.router import get_current_user
from src.bookmark.service import create, delete, get_bookmarked_profiles

from src.auth.unit_of_work import SqlAlchemyUnitOfWork as UserUow
from src.profile.unit_of_work import SqlAlchemyUnitOfWork as ProfileUow
from src.bookmark.unit_of_work import SqlAlchemyUnitOfWork as BookmarkUow

from src.profile.schemas import ProfileRead


router = APIRouter()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
def create_bookmark(current_user: Annotated[User, Depends(get_current_user)], profile_id: str = Query(...)):
    try:
        create(UserUow(), ProfileUow(), BookmarkUow(), current_user.id, profile_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': str(e)}
        )
    return {}


@router.delete('/{profile_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(current_user: Annotated[User, Depends(get_current_user)], profile_id: str):
    try:
        delete(BookmarkUow(), current_user.id, profile_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': str(e)}
        )
    return {}


@router.get('', response_model=List[ProfileRead])
def get_bookmarks(current_user: Annotated[User, Depends(get_current_user)]):
    profiles = get_bookmarked_profiles(BookmarkUow(), current_user.id)
    if not profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': "User doesn't have any bookmarked profiles"}
        )
    return profiles
