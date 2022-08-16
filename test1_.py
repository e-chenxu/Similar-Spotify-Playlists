import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import data
import html
import re

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)
# results = sp.search(q='weezer', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#   print(idx, track['name'])
playlist_link = "https://open.spotify.com/playlist/37i9dQZF1EIXowNAwj6gjO"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
results = sp.playlist(playlist_URI)
# tracks = results['items']
# while results['next']:
#   results = sp.next(results)
#   tracks.extend(results['items'])

# track_list = []
# for x in tracks:
#    new_dict = {'Name': x['track']['name'], 'Artist': x['track']['artists'][0]['name'],
#               'Image': x['track']['album']['images']}
#   track_list.append(new_dict)
print(results['tracks']['total'])
a = results['description']
print(a)
b = html.unescape(results['description'])
print(b)
c = remove_tags(b)
print(c)



# gets number of song matches of 2 playlists
# get both track lists
track_list = data.get_tracks_from_pl("https://open.spotify.com/playlist/4YXr1VsIVKxOk5xYrZxGlT")
track_list_og = data.get_tracks_from_pl("https://open.spotify.com/playlist/6IVklb7nv3xPRcPCdWOqNV")
total_songs = len(track_list) + len(track_list_og)



# str = ""
# for x in track_list:
#    str += '"' + x['Name'] + '"'
#    str += '"' + x['Artist'] + '"'

# print(str)
