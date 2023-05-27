"""empty message

Revision ID: 8b6726ab8330
Revises: 7672f2ca165d
Create Date: 2023-05-27 10:15:03.883334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b6726ab8330'
down_revision = '7672f2ca165d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('file_path', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
