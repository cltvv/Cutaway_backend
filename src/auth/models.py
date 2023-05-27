from datetime import datetime
from typing import Set

from src.profile.models import Profile


class User:
    def __init__(self,
                 id: str,
                 username: str,
                 email: str,
                 hashed_password: str,
                 created_at: datetime = datetime.utcnow(),
                 profiles: Set[Profile] = set()):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at
        self.hashed_password = hashed_password
        self.profiles = profiles

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            self.id == other.id and
            self.username == other.username and
            self.email == other.email
        )

    def __hash__(self):
        return hash((self.username, self.email))

    def add_profile(self, profile: Profile):
        if len(self.profiles) >= 10:
            raise ValueError("Profile's limit exceeded")
        self.profiles.add(profile)
    
    # def add_bookmark(self, bookmark: Bookmark):
    #     if any(bk.bookmarked_profile == bookmark.bookmarked_profile for bk in self.bookmarks):
    #         raise ValueError("Profile is allready bookmarked")
    #     if (bookmark.bookmarked_profile in self.profiles):
    #         raise ValueError("Can't bookmark your own profile")
    #     self.bookmarks.add(bookmark)

    # def delete_bookmark(self, profile_id: str):
    #     bookmark_to_delete = None
    #     for bookmark in self.bookmarks:
    #         if bookmark.bookmarked_profile.id == profile_id:
    #             bookmark_to_delete = bookmark
    #             break
    #     if bookmark_to_delete is not None:
    #         self.bookmarks.remove(bookmark_to_delete)
    #     else:
    #         raise ValueError("Bookmark was not found for the given profile_id")
    