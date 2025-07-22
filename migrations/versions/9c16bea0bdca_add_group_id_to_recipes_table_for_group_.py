from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c16bea0bdca'
down_revision = '3fc48f8040d5'
branch_labels = None
depends_on = None


def upgrade():
    
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'groups', ['group_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('group_id')

    # ### end Alembic commands ###
