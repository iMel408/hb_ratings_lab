"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie

from sqlalchemy import func

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<user_id>')
def show_user_profile(user_id):
    """gets user profile"""

    user = User.query.filter_by(user_id=user_id).first()
    return render_template('user_profile.html', user=user)


@app.route('/movies')
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.movie_title).all()
    return render_template("movie_list.html", movies=movies)


@app.route('/movies/<movie_id>')
def show_movie_profile(movie_id):
    """gets movie profile"""

    movie = Movie.query.filter_by(movie_id=movie_id).first()

    user_id = session.get('user_id', '')

    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id,user_id=user_id).first()
    else:
        user_rating = None

    score_tups = db.session.query(Rating.score,func.count(Rating.rating_id)).filter_by(movie_id=movie_id).group_by("score").all()

    return render_template('movie_profile.html', movie=movie,
        user_rating=user_rating, score_tups=score_tups)


@app.route('/registration_form')
def registration_form():

    return render_template('registration_form.html')


@app.route('/registration', methods=['POST'])
def registration():

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user:
        print('user exists: {}'.format(email))
        flash('user exists')
        return redirect('/')
    else:
        user = User(email=email, password=password)

        db.session.add(user)
        db.session.commit()

        print('successfully added user: {}'.format(email))
        flash('user added')

        return redirect('/')


@app.route('/login_form')
def login_form():

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()

    if user:
        print('user exists: {}'.format(email))
        if user.password == password:
            session['user_id'] = user.user_id
            print(session)
            flash('Logged In')
            return redirect('/users/{}'.format(user.user_id))
        else:
            print('wrong pw: {}'.format(email))
            flash('wrong pw')
            return redirect('/login_form')
    else:
        flash('account not found. register!')
        return redirect('/registration_form')


@app.route('/logout')
def logout():
    del(session['user_id'])
    flash('Logged out')
    print(session)
    return redirect('/')


@app.route('/set_rating', methods=['POST'])
def set_rating():
    rating = request.form.get('rating')
    user_id = int(session.get('user_id'))
    movie_id = int(request.referrer.split('/')[-1])
    user_rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    
    if user_rating:
        user_rating.score = rating
    else:
        user_rating = Rating(user_id=user_id, movie_id=movie_id, score=rating)
        db.session.add(user_rating)
    db.session.commit()

    return redirect('/movies/{}'.format(movie_id))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
