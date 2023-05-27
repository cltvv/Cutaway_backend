from uuid import uuid4
from typing import List
from datetime import datetime

from src.auth.unit_of_work import AbstractUnitOfWork as UserUow
from src.profile.unit_of_work import AbstractUnitOfWork as ProfileUow
from src.bookmark.unit_of_work import AbstractUnitOfWork as BookmarkUow

from src.bookmark.models import Bookmark
from src.profile.models import Profile


def create(user_uow: UserUow,
           profile_uow: ProfileUow,
           bookmark_uow: BookmarkUow,
           user_id: str,
           bm_profile_id: str):

    with profile_uow:
        profile = profile_uow.profiles.getByID(bm_profile_id)
        profile_uow.commit()
    if not profile:
        raise ValueError("Profile with this id doesn't exist")

    with user_uow:
        user = user_uow.users.getByID(user_id)
        for user_profile in user.profiles:
            if user_profile.id == bm_profile_id:
                raise ValueError("Can't bookmark your own profile")
        user_uow.commit()

    new_bookmark = Bookmark(id=uuid4(), user=user,
                            profile=profile, created_at=datetime.utcnow())

    with bookmark_uow:
        user_bookmarks = bookmark_uow.bookmarks.getByUserID(user_id)
        for user_bookmark in user_bookmarks:
            if user_bookmark.bookmarked_profile.id == bm_profile_id:
                raise ValueError("Can't bookmark the same profile twice")
        bookmark_uow.bookmarks.add(new_bookmark)
        bookmark_uow.commit()


def delete(bookmark_uow: BookmarkUow, user_id: str, bm_profile_id: str) -> None:
    with bookmark_uow:
        bookmarks = bookmark_uow.bookmarks.getByUserID(user_id)
        profile = None
        for bookmark in bookmarks:
            if bookmark.bookmarked_profile.id == bm_profile_id:
                profile = bookmark.bookmarked_profile
                break

        if not profile:
            raise ValueError(
                "User doesn't have any bookmarked profiles with this id")

        bookmark_uow.bookmarks.deleteByProfileID(bm_profile_id)
        bookmark_uow.commit()


def get_bookmarked_profiles(bookmark_uow: BookmarkUow, user_id: str) -> List[Profile]:
    with bookmark_uow:
        bookmarks = bookmark_uow.bookmarks.getByUserID(user_id)
        bookmarks = sorted(bookmarks, key=lambda x: x.created_at)
        profiles = [bookmark.bookmarked_profile for bookmark in bookmarks]
        bookmark_uow.commit()
    return profiles
