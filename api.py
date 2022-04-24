import requests
import json
from pprint import pprint

from config import key

def get_from_api(pl_id, current_vid):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"\
            "?part=snippet&playlistId={}"\
            "&key={}"\
            "&maxResults={}"\
            "&pageToken={}"\
            .format(pl_id, key, 1, current_vid)

    data = json.loads(requests.get(url).text)
    
    title = data["items"][0]["snippet"]["title"]
    current_vid = data["items"][0]["snippet"]["resourceId"]["videoId"]
    next_page = data["nextPageToken"]

    try:
        prev_page = data["prevPageToken"]
    except:
        prev_page = None
    
    return title, current_vid, prev_page, next_page, pl_id

def get_playlist_title(pl_id):
    url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={}&key={}&pageToken=".format(pl_id, key)
    data = json.loads(requests.get(url).text)
    title = data["items"][0]["snippet"]["localized"]["title"]
    return title
    
    