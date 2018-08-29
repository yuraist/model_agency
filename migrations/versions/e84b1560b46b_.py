"""empty message

Revision ID: e84b1560b46b
Revises: 23c5319f0069
Create Date: 2018-08-29 07:48:22.391151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e84b1560b46b'
down_revision = '23c5319f0069'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('photos_model_id_fkey', 'photos', type_='foreignkey')
    op.drop_column('photos', 'model_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('model_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('photos_model_id_fkey', 'photos', 'models', ['model_id'], ['id'])
    # ### end Alembic commands ###
