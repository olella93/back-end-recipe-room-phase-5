"""Create User table

Revision ID: 0767966cf727
Revises: 
Create Date: 2025-07-18 00:51:12.973179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0767966cf727'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=True),
        sa.Column('profile_image', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    # Drop users table
    op.drop_table('users')
