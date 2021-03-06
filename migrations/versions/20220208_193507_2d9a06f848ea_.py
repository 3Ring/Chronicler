"""Update images

Revision ID: 2d9a06f848ea
Revises: b4d0ccba3876
Create Date: 2022-02-08 19:35:07.184217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d9a06f848ea'
down_revision = 'b4d0ccba3876'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'img', new_column_name='img_string')
    op.add_column('images', sa.Column('removed', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'img_string', new_column_name='img')
    op.drop_column('images', 'removed')
    # ### end Alembic commands ###
