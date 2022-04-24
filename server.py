from flask import *
from api import *

app = Flask(__name__)

cookie_timeout = 60*60*24*365*10

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        playlist_data = request.cookies.get("playlists")
        if not playlist_data:
            playlist_data = ""

        titles = []
        playlists = []

        for pl in playlist_data.split(";"):
            if pl:
                titles.append(get_playlist_title(pl))
                playlists.append(pl)


        return render_template("index.html", data=zip(playlists, titles))
    else:
        url = request.form["playlist_url"]
        pl_id = url[url.index("?list=")+6:]

        resp = make_response(redirect("/playlist/"+pl_id)) 
        playlists = request.cookies.get("playlists")

        if playlists:
            resp.set_cookie("playlists", "{};{}".format(playlists, pl_id), max_age=cookie_timeout)
        else:
            resp.set_cookie("playlists", "{}".format(pl_id), max_age=cookie_timeout)

        return resp

@app.route("/delete/<playlist_id>")
def delete(playlist_id):
    playlist_data = request.cookies.get("playlists")

    resp = make_response(redirect("/"))
    try:
        playlist_data = playlist_data.replace(playlist_id, "")
        resp.set_cookie("playlists", playlist_data, max_age=cookie_timeout)
        resp.set_cookie("current_{}".format(playlist_id), "", expires=0)
        resp.set_cookie("seconds_{}".format(playlist_id), "", expires=0)
    except:
        pass
    
    return resp



@app.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    current_vid = request.cookies.get("current_{}".format(playlist_id))
    current_time = request.cookies.get("seconds_{}".format(playlist_id))

    if current_vid:
        elements = get_from_api(playlist_id, current_vid)
    else:
        elements = get_from_api(playlist_id, "")

    if not current_time:
        current_time = 0

    return(render_template("player.html", \
                    title=elements[0], \
                    vid=elements[1], \
                    prev_page=elements[2], \
                    next_page=elements[3], \
                    playlist=elements[4], \
                    start=current_time))

@app.route("/setvideo/<playlist>/<token>")
def setvideo(playlist, token):
    resp = make_response(redirect("/playlist/{}".format(playlist)))
    resp.set_cookie("current_{}".format(playlist), token, max_age=cookie_timeout)
    resp.set_cookie("seconds_{}".format(playlist), "0", max_age=cookie_timeout)
    return resp

@app.route("/settime/<playlist>/<seconds>")
def settime(playlist, seconds):
    resp = make_response(redirect("/playlist/{}".format(playlist)))
    resp.set_cookie("seconds_{}".format(playlist), seconds, max_age=cookie_timeout)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)