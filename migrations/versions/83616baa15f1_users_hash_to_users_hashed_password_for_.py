"""Users.hash to Users.hashed_password for clairity

Revision ID: 83616baa15f1
Revises: f7f3d8a8158a
Create Date: 2021-11-06 19:01:27.346386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83616baa15f1'
down_revision = 'f7f3d8a8158a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hash', new_column_name='hashed_password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password', new_column_name='hash')
    # ### end Alembic commands ###
