"""empty message

Revision ID: 69c19262ee71
Revises: 5606f7deb145
Create Date: 2022-08-11 20:20:46.192521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69c19262ee71'
down_revision = '5606f7deb145'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist_Available_Days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_available', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Artist_Available_Days')
    # ### end Alembic commands ###
