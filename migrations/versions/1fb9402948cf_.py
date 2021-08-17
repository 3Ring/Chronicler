"""empty message

Revision ID: 1fb9402948cf
Revises: 
Create Date: 2021-08-17 13:30:07.029222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fb9402948cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('hash', sa.String(length=120), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('imglink', sa.String(length=200), nullable=False),
    sa.Column('sessions', sa.Integer(), nullable=False),
    sa.Column('secret', sa.Integer(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('dm_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dm_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('imglink', sa.String(length=200), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('platinum', sa.Integer(), nullable=True),
    sa.Column('gold', sa.Integer(), nullable=True),
    sa.Column('electrum', sa.Integer(), nullable=True),
    sa.Column('silver', sa.Integer(), nullable=True),
    sa.Column('copper', sa.Integer(), nullable=True),
    sa.Column('experience', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('dexterity', sa.Integer(), nullable=True),
    sa.Column('constitution', sa.Integer(), nullable=True),
    sa.Column('intelligence', sa.Integer(), nullable=True),
    sa.Column('wisdom', sa.Integer(), nullable=True),
    sa.Column('charisma', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('secret_bio', sa.Text(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('games_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['games_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('synopsis', sa.Text(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('games_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['games_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('copper_value', sa.Integer(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['characters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('charname', sa.String(length=50), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('session_number', sa.Integer(), nullable=True),
    sa.Column('private', sa.Boolean(), nullable=True),
    sa.Column('in_character', sa.Boolean(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('character', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('np_cs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('secret_name', sa.String(length=40), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('secret_bio', sa.Text(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('np_cs')
    op.drop_table('notes')
    op.drop_table('loot')
    op.drop_table('sessions')
    op.drop_table('players')
    op.drop_table('places')
    op.drop_table('characters')
    op.drop_table('games')
    op.drop_table('users')
    op.drop_table('test')
    # ### end Alembic commands ###
