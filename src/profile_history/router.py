from fastapi import APIRouter, Depends, status, HTTPException, Query
from typing import Annotated, List

from src.auth.models import User
from src.auth.router import get_current_user
from src.profile_history.service import create, delete, get_historized_profiles

from src.auth.unit_of_work import SqlAlchemyUnitOfWork as UserUow
from src.profile.unit_of_work import SqlAlchemyUnitOfWork as ProfileUow
from src.profile_history.unit_of_work import SqlAlchemyUnitOfWork as HistoryProfileUow

from src.profile.schemas import ProfileRead

router = APIRouter()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
def add_profile_to_history(current_user: Annotated[User, Depends(get_current_user)], profile_id: str = Query(...)):
    try:
        create(UserUow(), ProfileUow(), HistoryProfileUow(), current_user.id, profile_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': str(e)}
        )
    return {}


@router.delete('/{profile_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_from_history(current_user: Annotated[User, Depends(get_current_user)], profile_id: str):
    try:
        delete(HistoryProfileUow(), current_user.id, profile_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': str(e)}
        )
    return {}


@router.get('', response_model=List[ProfileRead])
def get_history_profiles(current_user: Annotated[User, Depends(get_current_user)]):
    profiles = get_historized_profiles(HistoryProfileUow(), current_user.id)
    if not profiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': "User doesn't have any profiles in his history"}
        )
    return profiles