"""adding users

Revision ID: ce0cd2f9c6f9
Revises: 521c87414c01
Create Date: 2021-07-07 15:51:46.457192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce0cd2f9c6f9'
down_revision = '521c87414c01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('user_name', sa.String(length=8), nullable=True),
    sa.Column('password', sa.String(length=254), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_index(op.f('ix_users_date_of_birth'), 'users', ['date_of_birth'], unique=False)
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('street', sa.String(length=20), nullable=False),
    sa.Column('zip', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phone_numbers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phone_numbers')
    op.drop_table('addresses')
    op.drop_index(op.f('ix_users_date_of_birth'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###