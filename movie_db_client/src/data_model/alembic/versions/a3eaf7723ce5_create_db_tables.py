"""create db tables

Revision ID: a3eaf7723ce5
Revises: 
Create Date: 2024-07-16 15:28:26.478149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3eaf7723ce5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
            'directors',
            sa.Column('director_id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('dob', sa.Date, nullable=True),
            sa.Column('bio', sa.Text, nullable=True),
            sa.Column('nationality', sa.String(50), nullable=True),
            sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
        )

    # Create Writers table
    op.create_table(
        'writers',
        sa.Column('writer_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('nationality', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Studios table
    op.create_table(
        'studios',
        sa.Column('studio_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('founded', sa.Date, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Distributors table
    op.create_table(
        'distributors',
        sa.Column('distributor_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Actors table
    op.create_table(
        'actors',
        sa.Column('actor_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('nationality', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Genres table
    op.create_table(
        'genres',
        sa.Column('genre_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Movies table
    op.create_table(
        'movies',
        sa.Column('movie_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('original_title', sa.String(255), nullable=True),
        sa.Column('tagline', sa.String(255), nullable=True),
        sa.Column('plot', sa.Text, nullable=True),
        sa.Column('language', sa.String(50), nullable=True),
        sa.Column('country', sa.String(50), nullable=True),
        sa.Column('release_date', sa.Date, nullable=True),
        sa.Column('runtime', sa.Integer, nullable=True),
        sa.Column('budget', sa.Numeric(15, 2), nullable=True),
        sa.Column('box_office', sa.Numeric(15, 2), nullable=True),
        sa.Column('rating', sa.Numeric(3, 1), nullable=True),
        sa.Column('rating_count', sa.Integer, nullable=True),
        sa.Column('director_id', sa.Integer, sa.ForeignKey('directors.director_id'), nullable=True),
        sa.Column('writer_id', sa.Integer, sa.ForeignKey('writers.writer_id'), nullable=True),
        sa.Column('studio_id', sa.Integer, sa.ForeignKey('studios.studio_id'), nullable=True),
        sa.Column('distributor_id', sa.Integer, sa.ForeignKey('distributors.distributor_id'), nullable=True),
        sa.Column('poster_url', sa.String(255), nullable=True),
        sa.Column('trailer_url', sa.String(255), nullable=True),
        sa.Column('age_rating', sa.String(10), nullable=True),
        sa.Column('imdb_id', sa.String(50), nullable=True),
        sa.Column('tmdb_id', sa.String(50), nullable=True),
        sa.Column('homepage', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Ratings table
    op.create_table(
        'ratings',
        sa.Column('rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.movie_id'), nullable=False),
        sa.Column('source', sa.String(255), nullable=False),
        sa.Column('score', sa.Numeric(3, 1), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Cast table
    op.create_table(
        'cast',
        sa.Column('cast_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.movie_id'), nullable=False),
        sa.Column('actor_id', sa.Integer, sa.ForeignKey('actors.actor_id'), nullable=False),
        sa.Column('role', sa.String(255), nullable=False),
        sa.Column('billing_order', sa.Integer, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Movie_Genres table
    op.create_table(
        'movie_genres',
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.movie_id'), primary_key=True),
        sa.Column('genre_id', sa.Integer, sa.ForeignKey('genres.genre_id'), primary_key=True)
    )


def downgrade() -> None:
    pass
