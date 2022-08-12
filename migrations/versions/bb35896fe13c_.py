"""empty message

Revision ID: bb35896fe13c
Revises: 0e1ed864d936
Create Date: 2022-08-10 11:43:42.988503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb35896fe13c'
down_revision = '0e1ed864d936'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'updated_at')
    op.drop_column('Show', 'created_at')
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('Show', sa.Column('created_at', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('Show', sa.Column('updated_at', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###