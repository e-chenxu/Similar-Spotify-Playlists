from flask import Flask, request, render_template
import data

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        spotify_link = request.form.get("link")
        search_algo = request.form.get("box")
        print(search_algo)

        if not data.correct_link_check(spotify_link):
            return '', 204

        playlist_list = data.get_playlists(spotify_link, search_algo)
        your_playlist = data.get_playlist_info(spotify_link)

        return render_template("index.html", spotify_link=spotify_link,
                               your_playlist=your_playlist,
                               playlist_list=playlist_list, search_algo=search_algo)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
