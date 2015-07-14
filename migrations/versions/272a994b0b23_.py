"""empty message

Revision ID: 272a994b0b23
Revises: e870906fd
Create Date: 2015-07-12 15:19:02.277698

"""

# revision identifiers, used by Alembic.
revision = '272a994b0b23'
down_revision = 'e870906fd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'about_me',
               existing_type=sa.TEXT(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'about_me',
               existing_type=sa.TEXT(),
               nullable=True)
    ### end Alembic commands ###