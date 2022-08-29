from flask import Flask, request, render_template
import data

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        spotify_link = request.form.get("link")
        search_value = request.form.get("box")
        print(spotify_link, search_value)

        # check if the input is correct, if it isnt, dont do anything
        if not data.correct_link_check(spotify_link):
            return '', 204
        print('This is standard output')

        # now that we have the the spotify playlist link, we have to find 5 similar playlists

        playlist_list = data.get_five_playlists(spotify_link)
        your_playlist = data.get_playlist_info(spotify_link)
        return render_template("index.html", spotify_link=spotify_link,
                               your_playlist=your_playlist,
                               playlist_list=playlist_list)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
