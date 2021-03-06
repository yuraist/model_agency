"""empty message

Revision ID: 649cbcebcd08
Revises: 5a121e9f6ce7
Create Date: 2018-08-05 10:33:58.244792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '649cbcebcd08'
down_revision = '5a121e9f6ce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contracts', sa.Column('manager_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contracts', 'users', ['manager_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contracts', type_='foreignkey')
    op.drop_column('contracts', 'manager_id')
    # ### end Alembic commands ###
