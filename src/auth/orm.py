from datetime import datetime
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    String,
    TIMESTAMP,
    Boolean,
)


metadata = MetaData()


user = Table(
    'users',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('username', String(32), nullable=False, unique=True),
    Column('email', String(255), nullable=False, unique=True),
    Column('hashed_password', String(60), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow()),
)
