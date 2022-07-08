import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

#results = sp.search(q='weezer', limit=20)
#for idx, track in enumerate(results['tracks']['items']):
 #   print(idx, track['name'])
playlist_link = "https://open.spotify.com/playlist/2BqPbdxV1d3NlhMxJeoKAB"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
results = sp.playlist_items("4YXr1VsIVKxOk5xYrZxGlT",)
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

track_list = []
for x in tracks:
    new_dict = {}
    new_dict['Name'] = x['track']['name']
    new_dict['Artist'] = x['track']['artists'][0]['name']
    new_dict['Image'] = x['track']['album']['images'][2]['url']
    track_list.append(new_dict)
print(track_list)