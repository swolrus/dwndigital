"""buyer namefix

Revision ID: 84b254155ff2
Revises: e629e9a98bbe
Create Date: 2021-06-17 20:46:43.789370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84b254155ff2'
down_revision = 'e629e9a98bbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('buyer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=64), nullable=False))
        batch_op.drop_column('fullname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('buyer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fullname', sa.VARCHAR(length=64), nullable=False))
        batch_op.drop_column('name')

    # ### end Alembic commands ###
