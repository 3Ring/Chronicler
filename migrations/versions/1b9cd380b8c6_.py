"""empty message

Revision ID: 1b9cd380b8c6
Revises: 8acaafd40b1a
Create Date: 2021-09-05 10:06:34.874189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b9cd380b8c6'
down_revision = '8acaafd40b1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('imglink', sa.Text(), nullable=True))
    op.add_column('games', sa.Column('imglink', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'imglink')
    op.drop_column('characters', 'imglink')
    # ### end Alembic commands ###