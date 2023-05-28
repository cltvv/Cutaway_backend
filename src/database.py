from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, column_property, registry, relationship

from src.auth.orm import user
from src.profile.orm import profile, link
from src.bookmark.orm import bookmark
from src.search_query.orm import search_query
from src.profile_history.orm import history_profile
from src.image.orm import image
from src.auth.models import User
from src.profile.models import Profile, Link
from src.bookmark.models import Bookmark
from src.profile_history.models import HistoryProfile
from src.search_query.models import SearchQuery
from src.image.models import Image

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


def start_mappers():
    mapper_registry = registry()
    # MARKER 5: decoupling SqlAlphemy entities
    # by mapping them to domain versions
    link_mapper = mapper_registry.map_imperatively(Link, link)
    image_mapper = mapper_registry.map_imperatively(Image, image)
    profile_mapper = mapper_registry.map_imperatively(
        Profile,
        profile,
        properties={
            'links': relationship(link_mapper, collection_class=set, cascade="all, delete-orphan"),
            'bookmarks': relationship(
                Bookmark,
                backref='bookmarked_profile',
                cascade="all, delete",
                passive_deletes=True
            ),
            'history_profiles': relationship(
                HistoryProfile,
                backref='profile',
                cascade="all, delete",
                passive_deletes=True
            )
        })
    user_mapper = mapper_registry.map_imperatively(
        User,
        user,
        properties={
            'profiles': relationship(profile_mapper, collection_class=set, cascade="all, delete-orphan")
            # 'bookmarks': relationship('Bookmark', collection_class=set, back_populates='owner')
        }
    )
    bookmark_mapper = mapper_registry.map_imperatively(
        Bookmark,
        bookmark,
        properties={
            'owner': relationship(user_mapper)
        }
    )
    profile_history_mapper = mapper_registry.map_imperatively(
        HistoryProfile,
        history_profile,
        properties={
            'owner': relationship(user_mapper)
        }
    )
    search_query_mapper = mapper_registry.map_imperatively(
        SearchQuery,
        search_query,
        properties={
            'owner': relationship(user_mapper)
        }
    )


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    ),
    expire_on_commit=False
)
