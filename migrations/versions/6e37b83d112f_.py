"""empty message

Revision ID: 6e37b83d112f
Revises: 373b28e97f76
Create Date: 2018-08-22 14:02:21.547501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e37b83d112f'
down_revision = '373b28e97f76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_root', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_root')
    # ### end Alembic commands ###