"""empty message

Revision ID: 4812b606bc99
Revises: 
Create Date: 2017-12-08 14:26:54.129227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4812b606bc99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('icon', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rid', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_rid'), 'posts', ['rid'], unique=False)
    op.create_table('replys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_reply',
    sa.Column('posts_id', sa.Integer(), nullable=True),
    sa.Column('replys_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['posts_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['replys_id'], ['replys.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_reply')
    op.drop_table('replys')
    op.drop_index(op.f('ix_posts_rid'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
