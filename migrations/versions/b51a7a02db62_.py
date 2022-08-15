"""empty message

Revision ID: b51a7a02db62
Revises: 6344e6213966
Create Date: 2022-08-15 14:13:42.575403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b51a7a02db62'
down_revision = '6344e6213966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###