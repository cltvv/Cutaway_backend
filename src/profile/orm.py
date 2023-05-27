from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    TIMESTAMP
)

from src.auth.orm import metadata


profile = Table(
    'profiles',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('name', String(16), nullable=False),
    Column('lastname', String(16)),
    Column('profile_picture', String(255)),
    Column('phone_number', String(20)),
    Column('email', String(40)),
    Column('banner', String(255)),
    Column('place_of_work', String(40)),
    Column('education', String(40)),
    Column('created_at', TIMESTAMP, default=datetime.utcnow(), nullable=False),
    Column('owner_id', ForeignKey('users.id'), nullable=False)
)


link = Table(
    'links',
    metadata,
    Column('id', String(36), primary_key=True),
    Column('url', String(255), nullable=False),
    Column('title', String(255), nullable=False),
    Column('link_type', String(255), nullable=False),
    Column('order', Integer, nullable=False),
    Column('profile_id', ForeignKey('profiles.id')),
)

