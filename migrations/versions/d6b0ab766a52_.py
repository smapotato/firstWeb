"""empty message

Revision ID: d6b0ab766a52
Revises: 82b6aab9368f
Create Date: 2018-02-11 11:04:45.082457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6b0ab766a52'
down_revision = '82b6aab9368f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.String(length=100), nullable=False))
    op.create_foreign_key(None, 'post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###