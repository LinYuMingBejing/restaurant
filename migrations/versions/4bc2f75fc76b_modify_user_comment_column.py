"""modify user_comment column

Revision ID: 4bc2f75fc76b
Revises: 29d9faec506e
Create Date: 2019-08-17 07:27:05.010040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4bc2f75fc76b'
down_revision = '29d9faec506e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('store_id', sa.Integer(), nullable=True))
    op.drop_constraint('comment_ibfk_2', 'comment', type_='foreignkey')
    op.create_foreign_key(None, 'comment', 'ta', ['store_id'], ['id'])
    op.drop_column('comment', 'restaurant')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('restaurant', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.create_foreign_key('comment_ibfk_2', 'comment', 'ta', ['restaurant'], ['id'])
    op.drop_column('comment', 'store_id')
    # ### end Alembic commands ###