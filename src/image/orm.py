from sqlalchemy import (
    Table,
    Column,
    String
)

from src.profile_history.orm import metadata

image = Table(
    'images',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('file_path', String(255), nullable=False)
)
