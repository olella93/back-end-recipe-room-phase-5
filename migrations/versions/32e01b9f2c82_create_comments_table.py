from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32e01b9f2c82'
down_revision = '9c16bea0bdca'
branch_labels = None
depends_on = None


def upgrade():
   
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    
    op.drop_table('comments')
    # ### end Alembic commands ###
