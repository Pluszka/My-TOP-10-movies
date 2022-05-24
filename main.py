from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FilmList.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, unique=True, nullable=True)
    review = db.Column(db.String(250), unique=True, nullable=True)
    img_url = db.Column(db.String(250), unique=True, nullable=False)


class editRating(FlaskForm):
    rating = StringField('New rating', validators=[DataRequired()])
    review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField()


#db.create_all()

# new = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new)
# db.session.commit()

@app.route("/")
def home():
    movieList = db.session.query(Movie).all()
    return render_template("index.html", top10=movieList)


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    reviewform = editRating()
    movieid = request.args.get("id")
    movie = Movie.query.get(movieid)
    if reviewform.validate_on_submit():
        movie.rating = float(reviewform.rating.data)
        movie.review = reviewform.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=reviewform, id=movie)


@app.route('/del')
def delete():
    idnum = request.args.get("id")
    movie = Movie.query.get(idnum)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
