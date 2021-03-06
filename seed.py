"""Utility file to seed ratings database from MovieLens data in seed_data/"""
from datetime import datetime
from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    gender=gender,
                    occupation=occupation,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()

def create_genres():
    genres = ['unknown', 'action', 'adventure', 'animation', 'childrens', 'comedy', 'crime', 
              'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical', 'mystery', 
              'romance', 'sci_fi', 'thriller', 'war', 'western']

    # genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # genre_name = db.Column(db.String(20), nullable=False)
    # Genre(db.Model):

    Genre.query.delete()

    for genre in genres:
        genre_to_save = Genre(genre_name=genre)
        db.session.add(genre_to_save)

    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""
    print("Movies")

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        movie_id, movie_title, release_date, video_release_date, imdb_url,\
        unknown, action, adventure, animation,childrens, comedy, crime,\
        documentary, drama, fantasy, film_noir, horror, musical, mystery,\
        romance, sci_fi, thriller, war, western = row.split("|")

        if release_date:
            release_date = datetime.strptime(release_date, '%d-%b-%Y')
        else:
            release_date = None

        if video_release_date:
            video_release_date = datetime.strptime(video_release_date, '%d-%b-%Y')
        else:
            video_release_date = None

        movie_title = movie_title.rpartition(' (')[0]

        movie = Movie(movie_id=movie_id,
                      movie_title=movie_title,
                      release_date=release_date,
                      video_release_date=video_release_date,
                      imdb_url=imdb_url)

        db.session.add(movie)

    db.session.commit()

    # moviegenre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    # genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)


        # movie_genre = MovieGenre(movie_id=movie_id,
        #                          unknown=unknown,
        #                          action=action,
        #                          adventure=adventure,
        #                          animation=animation,
        #                          childrens=childrens,
        #                          comedy=comedy,
        #                          crime=crime,
        #                          documentary=documentary,
        #                          drama=drama,
        #                          fantasy=fantasy,
        #                          film_noir=film_noir,
        #                          horror=horror,
        #                          musical=musical,
        #                          mystery=mystery,
        #                          romance=romance,
        #                          sci_fi=sci_fi,
        #                          thriller=thriller,
        #                          war=war,
        #                          western=western)

def load_ratings():
    """Load ratings from u.data into database."""
    print("Ratings")

    Rating.query.delete()


    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, movie_id, score, timestamp = row.split("\t")
        timestamp = datetime.fromtimestamp(int(timestamp))

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score,
                        timestamp=timestamp)


        db.session.add(rating)
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
