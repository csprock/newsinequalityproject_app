"""empty message

Revision ID: 1988c96251a3
Revises: bcc68a5b1c73
Create Date: 2019-05-16 21:09:45.055489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1988c96251a3'
down_revision = 'bcc68a5b1c73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('header_pic', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'header_pic')
    # ### end Alembic commands ###
