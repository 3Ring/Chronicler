"""empty message

Revision ID: 7f7aea39c0b1
Revises: 6590df97027d
Create Date: 2021-07-24 19:49:07.555883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f7aea39c0b1'
down_revision = '6590df97027d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('charname', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notes', 'charname')
    # ### end Alembic commands ###