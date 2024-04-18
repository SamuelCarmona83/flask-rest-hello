"""empty message

Revision ID: 151c8a9d3e8b
Revises: a5cffa318ac2
Create Date: 2024-03-21 01:38:04.339082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '151c8a9d3e8b'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drink',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=380), nullable=False),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drink')
    # ### end Alembic commands ###