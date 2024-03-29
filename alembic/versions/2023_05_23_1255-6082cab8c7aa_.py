"""empty message

Revision ID: 6082cab8c7aa
Revises: f1172fa8ff94
Create Date: 2023-05-23 12:55:56.049505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6082cab8c7aa'
down_revision = 'f1172fa8ff94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookmarks', 'profile_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=True)
    op.drop_constraint('bookmarks_profile_id_fkey', 'bookmarks', type_='foreignkey')
    op.create_foreign_key(None, 'bookmarks', 'profiles', ['profile_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.create_foreign_key('bookmarks_profile_id_fkey', 'bookmarks', 'profiles', ['profile_id'], ['id'])
    op.alter_column('bookmarks', 'profile_id',
               existing_type=sa.VARCHAR(length=36),
               nullable=False)
    # ### end Alembic commands ###
