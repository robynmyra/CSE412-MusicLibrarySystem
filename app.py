import os
from datetime import datetime
from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, validators, SubmitField
from wtforms.validators import DataRequired
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "password"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

# Create Form Class
class SearchForm(FlaskForm):
    searchString = StringField("Search", validators=[DataRequired()])
    artistsButton = SubmitField("Artists")
    songsButton = SubmitField("Songs")
    albumsButton = SubmitField("Albums")

@app.route('/', methods=['GET', 'POST'])
def index():
    searchString = None
    artists = None
    songs = None
    albums = None
    form = SearchForm()
    if form.validate_on_submit():
        searchString = form.searchString.data
        #form.searchString.data = ''
        if form.artistsButton.data:
            cur.execute('SELECT * FROM artists WHERE artists.name ILIKE %s ORDER BY artists.followers DESC', ('%'+searchString+'%',))
            artists = cur.fetchall()
        elif form.songsButton.data:
            cur.execute('SELECT sg.song_name as song, al.name as album, ar.name, sg.song_type as artist FROM songs as sg, albums as al, artists as ar, releases as rl, tracks as tr WHERE sg.song_id = tr.song_id and tr.album_id = al.album_id and al.album_id = rl.album_id and rl.artist_id = ar.artist_id and sg.song_name ILIKE %s ORDER BY sg.popularity DESC', ('%'+searchString+'%',))
            songs = cur.fetchall()
        elif form.albumsButton.data:
            cur.execute('SELECT distinct al.album_id, al.name as album, ar.name as name, al.total_tracks, ar.main_genre, al.popularity FROM songs as sg, albums as al, artists as ar, releases as rl, tracks as tr WHERE sg.song_id = tr.song_id and tr.album_id = al.album_id and al.album_id = rl.album_id and rl.artist_id = ar.artist_id and al.name ILIKE %s ORDER BY al.popularity DESC', ('%'+searchString+'%',))
            albums = cur.fetchall()

    return render_template('layout.html', searchString = searchString, form = form, artists=artists, songs=songs, albums=albums)

if __name__ == "__main__":
    app.run(debug=True)
