"""create initial tables

Revision ID: 6b0f65269604
Revises: 
Create Date: 2025-09-30 21:15:09.006951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b0f65269604'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    # Movies table
    op.create_table('movies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('genre', sa.String(), nullable=False),
        sa.Column('release_year', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('ratings_count', sa.Integer(), nullable=True),
        sa.Column('ratings_avg', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'])
    )
    op.create_index(op.f('ix_movies_genre'), 'movies', ['genre'], unique=False)
    op.create_index(op.f('ix_movies_id'), 'movies', ['id'], unique=False)
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)
    
    # Ratings table
    op.create_table('ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('review', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
        sa.UniqueConstraint('movie_id', 'user_id', name='unique_user_movie_rating')
    )
    op.create_index(op.f('ix_ratings_id'), 'ratings', ['id'], unique=False)

def downgrade():
    op.drop_table('ratings')
    op.drop_table('movies')
    op.drop_table('users')
