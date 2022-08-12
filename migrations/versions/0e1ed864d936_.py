"""empty message

Revision ID: 0e1ed864d936
Revises: b51be4c076ae
Create Date: 2022-08-10 11:41:08.737079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e1ed864d936'
down_revision = 'b51be4c076ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    op.drop_column('Show', 'updated_at')
    op.drop_column('Show', 'created_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('created_at', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.add_column('Show', sa.Column('updated_at', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('start_time', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    # ### end Alembic commands ###