"""Change 'loot' table to 'items'

Revision ID: 98069582e7e9
Revises: 3f318724cafa
Create Date: 2022-02-08 19:04:21.646494

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '98069582e7e9'
down_revision = '3f318724cafa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('loot', 'items')
    op.add_column('items', sa.Column('removed', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True))






def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'removed')
    op.rename_table('items', 'loot')
    # ### end Alembic commands ###