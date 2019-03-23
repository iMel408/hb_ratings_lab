"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    ratings = db.relationship('Rating')
    movies = db.relationship('Movie',
        secondary = 'ratings',
        back_populates = 'users')

    def __repr__(self):
        """Show info about usesr"""
        return f"<User user_id={self.user_id} email={self.email}>"
# Put your Movie and Rating model classes here.


class Movie(db.Model):

    __tablename__="movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    released_at = db.Column(db.DateTime, nullable=False)
    video_released_date = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(1000), nullable=True)

    ratings = db.relationship('Rating')
    users = db.relationship('User',
        secondary = 'ratings',
        back_populates = 'movies')
    genres = db.relationship('Genre',
        secondary = 'movie_genres',
        back_populates = 'movies')

    def __repr__(self):
        """Show info about movie"""
        return f"<Movie movie_id={self.movie_id} title={self.title}>"

class Rating(db.Model):

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

    movie = db.relationship('Movie', back_populates='ratings')
    user = db.relationship('User', back_populates='ratings')

    def __repr__(self):
        """Show info about rating"""
        return f"<Rating rating_id={self.rating_id} movie_id={self.movie_id} user_id={self.user_id} score={self.score}>"


class Genre(db.Model):

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String(20), nullable=False)

    movies = db.relationship('Movie',
        secondary = 'movie_genres',
        back_populates = 'genres')

    def __repr__(self):
        """Show info about Genre"""
        return f"<Genre genre_id={self.genre_id} genre={self.genre_name}>"



class MovieGenre(db.Model):

    __tablename__ = 'movie_genres'

    moviegenre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)

    movie = db.relationship('Movie')
    genre = db.relationship('Genre')

    def __repr__(self):
        """Show info about Movie-Genre"""
        return f"<MovieGenre movie_id={self.movie_id} genre_id={self.genre_id}>"




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")







for line in item:
    unk  = row[]
    ....

