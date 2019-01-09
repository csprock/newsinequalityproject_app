"""empty message

Revision ID: 2cd053da6867
Revises: 71759f91d2b2
Create Date: 2019-01-05 14:47:11.307485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cd053da6867'
down_revision = '71759f91d2b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('u_author_firstname_lastname', 'author', ['firstname', 'lastname'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('u_author_firstname_lastname', 'author', type_='unique')
    # ### end Alembic commands ###
