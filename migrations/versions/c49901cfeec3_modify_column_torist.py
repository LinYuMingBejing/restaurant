"""modify column torist 

Revision ID: c49901cfeec3
Revises: 51bac4a118cc
Create Date: 2019-08-12 16:09:37.918731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c49901cfeec3'
down_revision = '51bac4a118cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotel', sa.Column('tourist', sa.String(length=128), nullable=True))
    op.drop_column('hotel', 'tourist_1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotel', sa.Column('tourist_1', mysql.VARCHAR(length=128), nullable=True))
    op.drop_column('hotel', 'tourist')
    # ### end Alembic commands ###