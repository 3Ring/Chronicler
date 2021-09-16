"""empty message

Revision ID: c9da68d48a61
Revises: a05185dbccf4
Create Date: 2021-09-16 21:37:15.176717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9da68d48a61'
down_revision = 'a05185dbccf4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('img_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'characters', 'images', ['img_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'characters', type_='foreignkey')
    op.drop_column('characters', 'img_id')
    # ### end Alembic commands ###