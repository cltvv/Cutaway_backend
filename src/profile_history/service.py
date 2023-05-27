from uuid import uuid4
from typing import List
from datetime import datetime

from src.auth.unit_of_work import AbstractUnitOfWork as UserUow
from src.profile.unit_of_work import AbstractUnitOfWork as ProfileUow
from src.profile_history.unit_of_work import AbstractUnitOfWork as HistoryProfileUow


from src.profile_history.models import HistoryProfile
from src.profile.models import Profile


def create(user_uow: UserUow,
           profile_uow: ProfileUow,
           history_profile_uow: HistoryProfileUow,
           user_id: str,
           profile_id: str):

    with profile_uow:
        profile = profile_uow.profiles.getByID(profile_id)
        profile_uow.commit()
    if not profile:
        raise ValueError("Profile with this id doesn't exist")

    with user_uow:
        user = user_uow.users.getByID(user_id)
        for user_profile in user.profiles:
            if user_profile.id == profile_id:
                raise ValueError(
                    "Your own profile can't be added to profile history")
        user_uow.commit()

    new_history_profile = HistoryProfile(id=uuid4(), user=user,
                                         profile=profile, created_at=datetime.utcnow())

    with history_profile_uow:
        user_history = history_profile_uow.history_profiles.getByUserID(
            user_id)
        for user_historized_profile in user_history:
            if user_historized_profile.profile.id == profile_id:
                user_historized_profile.created_at = datetime.utcnow()
                history_profile_uow.commit()
                return
        history_profile_uow.history_profiles.add(new_history_profile)
        history_profile_uow.commit()


def delete(history_profile_uow: HistoryProfileUow, user_id: str, profile_id: str) -> None:
    with history_profile_uow:
        history_profiles = history_profile_uow.history_profiles.getByUserID(
            user_id)
        profile = None
        for history_profile in history_profiles:
            if history_profile.profile.id == profile_id:
                profile = history_profile.profile
                break

        if not profile:
            raise ValueError(
                "User doesn't have any profiles with this id in his history")
        history_profile_uow.history_profiles.deleteByProfileID(profile_id)
        history_profile_uow.commit()


def get_historized_profiles(history_profile_uow: HistoryProfileUow, user_id: str) -> List[Profile]:
    with history_profile_uow:
        history_profiles = history_profile_uow.history_profiles.getByUserID(user_id)
        history_profiles = sorted(history_profiles, key=lambda x: x.created_at)
        profiles = [history_profile.profile for history_profile in history_profiles]
        history_profile_uow.commit()
    return profiles