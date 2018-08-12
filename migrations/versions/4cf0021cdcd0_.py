"""empty message

Revision ID: 4cf0021cdcd0
Revises: 6806cba1823b
Create Date: 2018-08-12 18:54:28.690640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cf0021cdcd0'
down_revision = '6806cba1823b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'clubs', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clubs', type_='unique')
    # ### end Alembic commands ###