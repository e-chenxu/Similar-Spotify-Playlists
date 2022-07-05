from flask import Flask, request, render_template

app = Flask(__name__)

def emptyCheck():
    return

@app.route('/',methods =["GET", "POST"])
def index():
    if request.method == "POST":
       emptyCheck()
       # getting input with name = fname in HTML form
       spotify_link = request.form.get("link")
       return render_template("index.html", spotify_link = spotify_link)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)