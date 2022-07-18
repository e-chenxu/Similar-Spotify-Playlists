from flask import Flask, request, render_template
import data

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        spotify_link = request.form.get("link")

        # check if the input is correct, if it isnt, dont do anything
        if not data.correct_link_check(spotify_link):
            return '', 204

        track_list = data.get_tracks_from_pl(spotify_link)
        # now that we have the track_list, we have to find 5 similar playlists

        playlist_list = data.get_five_playlists(track_list)
        return render_template("index.html", spotify_link=spotify_link, track_list=track_list,
                               playlist_list=playlist_list)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
