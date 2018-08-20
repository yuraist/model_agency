"""empty message

Revision ID: 373b28e97f76
Revises: 4cf0021cdcd0
Create Date: 2018-08-19 17:24:58.766750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '373b28e97f76'
down_revision = '4cf0021cdcd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('models', sa.Column('next_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('models', 'next_date')
    # ### end Alembic commands ###