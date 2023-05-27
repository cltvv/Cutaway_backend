from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    String,
    ForeignKey,
    TIMESTAMP
)

from src.profile.orm import metadata

bookmark = Table(
    'bookmarks',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('owner_id', ForeignKey('users.id'), nullable=False),
    Column('profile_id', ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow(), nullable=False)
)