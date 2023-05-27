from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    String,
    ForeignKey,
    TIMESTAMP
)

from src.search_query.orm import metadata

history_profile = Table(
    'history_profiles',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('owner_id', ForeignKey('users.id'), nullable=False),
    Column('profile_id', ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow(), nullable=False)
)