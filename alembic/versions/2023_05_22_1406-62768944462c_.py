"""empty message

Revision ID: 62768944462c
Revises: 352039f368f0
Create Date: 2023-05-22 14:06:48.872359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62768944462c'
down_revision = '352039f368f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('place_of_work', sa.String(length=40), nullable=True))
    op.drop_column('profiles', 'job')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('job', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
    op.drop_column('profiles', 'place_of_work')
    # ### end Alembic commands ###
