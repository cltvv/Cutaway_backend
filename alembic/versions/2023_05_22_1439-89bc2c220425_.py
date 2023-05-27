"""empty message

Revision ID: 89bc2c220425
Revises: 62768944462c
Create Date: 2023-05-22 14:39:02.929197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89bc2c220425'
down_revision = '62768944462c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('links', 'order')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('links', sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###