"""注释

Revision ID: eeb9d028813c
Revises: a9de775c7805
Create Date: 2019-07-14 11:18:08.342697

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eeb9d028813c'
down_revision = 'a9de775c7805'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_user', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.drop_column('tb_user', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_user', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('tb_user', 'is_superuser')
    # ### end Alembic commands ###
