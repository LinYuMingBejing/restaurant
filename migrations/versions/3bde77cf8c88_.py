"""empty message

Revision ID: 3bde77cf8c88
Revises: eecc881fb4b7
Create Date: 2019-08-16 19:37:05.391225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bde77cf8c88'
down_revision = 'eecc881fb4b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('order_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservation', 'order_id')
    # ### end Alembic commands ###