from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca02473953e0'
down_revision = '32e01b9f2c82'
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table('bookmarks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    
    op.drop_table('bookmarks')
    # ### end Alembic commands ###
