from flask import Flask, render_template, request, url_for, redirect, abort, Response
import sqlite3 as sql

app = Flask(__name__)


def filmflixDBCon():
    conn = sql.connect("FlaskProject/FilmFlask/filmflix.db")
    conn.row_factory = sql.Row
    return conn


@app.route('/films')
def films():
    conn = filmflixDBCon()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tblFilms")
    getFilms = cursor.fetchall()
    return render_template('films.html', title="Films", filmsInDB=getFilms)


@app.route('/<int:filmID>/delete', methods=('POST',))
def delete(filmID):
    conn = filmflixDBCon()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tblFilms WHERE filmID = ?", (filmID, ))
    conn.commit()
    conn.close()
    return redirect(url_for('films'))


def getFilm(recordID):
    conn = filmflixDBCon()
    cursor = conn.cursor()
    aFilm = cursor.execute("SELECT * FROM tblFilms WHERE filmID = ?",
                           (recordID, )).fetchone()
    conn.close()
    if aFilm is None:
        abort(Response(f"No Record {aFilm} was found in db"))
    return aFilm


@app.route('/<int:filmID>/update', methods=('GET', 'POST'))
def update(filmID):
    aFilmRecord = getFilm(filmID)
    if request.method == 'POST':
        title = request.form['Title']
        yearReleased = request.form['yearReleased']
        rating = request.form['Rating']
        duration = request.form['Duration']
        genre = request.form['Genre']
        conn = filmflixDBCon()
        cursor = conn.cursor()
        cursor.execute("UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ?" 'WHERE filmID = ?',
                       (title, yearReleased, rating, duration, genre, filmID))
        conn.commit()
        conn.close()
        return redirect(url_for('films'))
    return render_template('updatefilms.html', title='Update Films', aFilmRecord=aFilmRecord)


@app.route('/addfilms', methods=['GET', 'POST'])
def addfilms():
    if request.method == 'POST':
        title = request.form['Title']
        yearReleased = request.form['yearReleased']
        rating = request.form['Rating']
        duration = request.form['Duration']
        genre = request.form['Genre']
        conn = filmflixDBCon()
        cursor = conn.cursor()
        filmID = cursor.lastrowid
        cursor.execute("INSERT INTO tblFilms VALUES (?,?,?,?,?,?)",
                       (filmID, title, yearReleased, rating, duration, genre))
        conn.commit()
        conn.close()
        return redirect(url_for('films'))
    return render_template('addfilms.html', title='Add Films')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/searchfilms')
def searchfilms():
    return render_template('searchfilms.html', title="Search")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8900)
