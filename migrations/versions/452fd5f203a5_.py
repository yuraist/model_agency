"""empty message

Revision ID: 452fd5f203a5
Revises: 6e37b83d112f
Create Date: 2018-08-22 19:10:09.469654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '452fd5f203a5'
down_revision = '6e37b83d112f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('models', sa.Column('period', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('models', 'period')
    # ### end Alembic commands ###
