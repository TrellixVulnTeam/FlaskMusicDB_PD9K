from flask import Flask, render_template, request, g
import sqlite3

DATABASE = 'data/music.db'
app = Flask(__name__)


def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/wildcard_result', methods=['POST', 'GET'])
def wildcard_result():
    response = []
    if request.method == "POST":
        wildcard_data = request.form
        print(wildcard_data["wild-data"])
        # query artists for match
        artists = query_db('SELECT stageName, genre1, genre2, idThumbNail FROM ARTISTS WHERE stageName = ?', [wildcard_data["wild-data"]])
        print(artists)
        if artists is not None:
            for artist in artists:
                result = dict()
                thumbnail = query_db('SELECT filename from THUMBNAIL WHERE idThumbNail = ?', [artist['idThumbNail']], one=True)
                result["thumbnail"] = thumbnail['filename']
                result["name"] = artist['stageName']
                result["details"] = artist['genre1'] + " & " + artist['genre2']
                print("result ", result)
                response.append(result)
        # query album for match
        albums = query_db("SELECT name, year, thumbnail FROM ALBUMS WHERE name = ?", [wildcard_data["wild-data"]])
        print(albums)
        if albums is not None:
            for album in albums:
                result = dict()
                thumbnail = query_db('SELECT filename from THUMBNAIL WHERE idThumbNail = ?', [album['idThumbNail']], one=True)
                result["thumbnail"] = thumbnail['filename']
                result["name"]: album['name']
                result["details"]: album['year']
                response.append(result)
        # query tracks for match
        tracks = query_db("SELECT trackName, genre1, genre2, year, idthumbnail FROM TRACKS WHERE trackName = ?", [wildcard_data["wild-data"]])
        print(tracks)
        if tracks is not None:
            for track in tracks:
                result = dict()
                thumbnail = query_db('SELECT filename from THUMBNAIL WHERE idThumbNail = ?', [track['idThumbNail']],
                                     one=True)
                result["thumbnail"] = thumbnail['filename']
                result["name"]: track['trackName']
                result["details"]: track['genre1'] + "/" + track['genre1'] + " " + track['year']
                response.append(result)
        print(response)
    return render_template('response.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)

