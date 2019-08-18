"""empty message

Revision ID: a3b0ffc51332
Revises: 21b654470056
Create Date: 2019-08-14 14:44:35.395688

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a3b0ffc51332'
down_revision = '21b654470056'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('reservation_ibfk_1', 'reservation', type_='foreignkey')
    op.drop_column('reservation', 'userid')
    op.add_column('user', sa.Column('reservation_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'reservation', ['reservation_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'reservation_id')
    op.add_column('reservation', sa.Column('userid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('reservation_ibfk_1', 'reservation', 'user', ['userid'], ['id'])
    # ### end Alembic commands ###