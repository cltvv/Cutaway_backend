from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    String,
    ForeignKey,
    TIMESTAMP
)

from src.bookmark.orm import metadata

search_query = Table(
    'search_queries',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('owner_id', ForeignKey('users.id'), nullable=False),
    Column('text_query', String(255), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow(), nullable=False)
)
