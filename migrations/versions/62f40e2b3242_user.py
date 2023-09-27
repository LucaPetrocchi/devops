"""user

Revision ID: 62f40e2b3242
Revises: e960f3c707ad
Create Date: 2023-08-08 21:11:08.789326

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '62f40e2b3242'
down_revision = 'e960f3c707ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('paises', schema=None) as batch_op:
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', mysql.VARCHAR(length=500), nullable=False))

    op.drop_table('users')
    # ### end Alembic commands ###
