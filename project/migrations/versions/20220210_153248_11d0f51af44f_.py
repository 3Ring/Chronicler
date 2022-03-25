"""remove game_id from chracters

Revision ID: 11d0f51af44f
Revises: 51c3bfee43e4
Create Date: 2022-02-10 15:32:48.522998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11d0f51af44f'
down_revision = '51c3bfee43e4'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # op.drop_constraint('characters_game_id_fkey', 'characters', type_='foreignkey')
    # op.drop_column('characters', 'game_id')


def downgrade():
    pass
    # op.add_column('characters', sa.Column('game_id', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=False))
    # op.create_foreign_key('characters_game_id_fkey', 'characters', 'games', ['game_id'], ['id'])
