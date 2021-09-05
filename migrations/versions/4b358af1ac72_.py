"""empty message

Revision ID: 4b358af1ac72
Revises: 5021e414436d
Create Date: 2021-09-05 09:59:38.897416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b358af1ac72'
down_revision = '5021e414436d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loot', sa.Column('copper_value', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loot', 'copper_value')
    # ### end Alembic commands ###
