"""empty message

Revision ID: c30794def686
Revises: b734cd0ea0ef
Create Date: 2018-02-09 10:06:23.984859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c30794def686'
down_revision = 'b734cd0ea0ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=False),
    sa.Column('link_url', sa.String(length=255), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner')
    # ### end Alembic commands ###
