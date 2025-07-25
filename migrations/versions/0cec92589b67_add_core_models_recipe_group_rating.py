from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cec92589b67'
down_revision = '0767966cf727'
branch_labels = None
depends_on = None


def upgrade():
   
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('ingredients', sa.Text(), nullable=False),
    sa.Column('instructions', sa.Text(), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('serving_size', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    
    op.drop_table('recipes')
    # ### end Alembic commands ###
