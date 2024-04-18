"""empty message

Revision ID: 164a8dc79a1c
Revises: 151c8a9d3e8b
Create Date: 2024-03-26 00:48:14.034845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '164a8dc79a1c'
down_revision = '151c8a9d3e8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_table_orders',
    sa.Column('orders', sa.Integer(), nullable=True),
    sa.Column('drink', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['drink'], ['drink.id'], ),
    sa.ForeignKeyConstraint(['orders'], ['orders.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_table_orders')
    op.drop_table('orders')
    # ### end Alembic commands ###
