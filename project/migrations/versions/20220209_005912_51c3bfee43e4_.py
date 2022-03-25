"""Update characters

Revision ID: 51c3bfee43e4
Revises: 59ae6e0b35cd
Create Date: 2022-02-09 00:59:12.488030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51c3bfee43e4'
down_revision = '59ae6e0b35cd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('characters', sa.Column('removed', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True))
    op.add_column('characters', sa.Column('avatar', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True))
    op.add_column('characters', sa.Column('dm', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True))
    op.add_column('characters', sa.Column('copy', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False))
    op.alter_column('characters', 'game_id', existing_type=sa.Integer(), nullable=True)
def downgrade():
    op.alter_column('characters', 'game_id', existing_type=sa.Integer(), nullable=False)
    op.drop_column('characters', 'copy')
    op.drop_column('characters', 'dm')
    op.drop_column('characters', 'avatar')
    op.drop_column('characters', 'removed')
