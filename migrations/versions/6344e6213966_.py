"""empty message

Revision ID: 6344e6213966
Revises: da25805561b4
Create Date: 2022-08-15 14:13:27.153640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6344e6213966'
down_revision = 'da25805561b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###