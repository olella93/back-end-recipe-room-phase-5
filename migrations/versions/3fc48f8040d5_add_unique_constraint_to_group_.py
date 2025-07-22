from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fc48f8040d5'
down_revision = '60006c5c12c0'
branch_labels = None
depends_on = None


def upgrade():
    
    with op.batch_alter_table('group_members', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_group_membership', ['user_id', 'group_id'])

    # ### end Alembic commands ###


def downgrade():
    
    with op.batch_alter_table('group_members', schema=None) as batch_op:
        batch_op.drop_constraint('unique_group_membership', type_='unique')

    # ### end Alembic commands ###
