from flask import Flask, request, render_template
import data

app = Flask(__name__)


def emptyCheck():
    return


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emptyCheck()
        # getting input with name = fname in HTML form
        spotify_link = request.form.get("link")
        track_list = data.get_tracks_from_pl(spotify_link)
        playlist_list = data.find_similar_playlists(track_list)
        return render_template("index.html", spotify_link=spotify_link, track_list=track_list, playlist_list=playlist_list)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
