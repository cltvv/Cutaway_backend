"""empty message

Revision ID: 66da8ef5de07
Revises: 8901db871631
Create Date: 2023-05-20 15:16:44.234857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66da8ef5de07'
down_revision = '8901db871631'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gallery_images')
    op.drop_table('galleries')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('galleries',
    sa.Column('id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('profile_id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], name='galleries_profile_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='galleries_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('gallery_images',
    sa.Column('id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('image', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('gallery_id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['gallery_id'], ['galleries.id'], name='gallery_images_gallery_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='gallery_images_pkey')
    )
    # ### end Alembic commands ###