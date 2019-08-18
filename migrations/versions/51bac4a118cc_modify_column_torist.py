"""modify column torist 

Revision ID: 51bac4a118cc
Revises: bb1e45215f13
Create Date: 2019-08-12 16:09:01.385492

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '51bac4a118cc'
down_revision = 'bb1e45215f13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotel', sa.Column('tourist_1', sa.String(length=128), nullable=True))
    op.drop_column('hotel', 'tourist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotel', sa.Column('tourist', mysql.VARCHAR(length=32), nullable=True))
    op.drop_column('hotel', 'tourist_1')
    # ### end Alembic commands ###