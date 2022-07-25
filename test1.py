import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

#results = sp.search(q='weezer', limit=20)
#for idx, track in enumerate(results['tracks']['items']):
 #   print(idx, track['name'])
playlist_link = "https://open.spotify.com/playlist/2DJd0WJmc7i7lrBeQNvmDM?si=1214bd29679b4d44"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
results = sp.playlist_items(playlist_URI)
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

track_list = []
for x in tracks:
    new_dict = {'Name': x['track']['name'], 'Artist': x['track']['artists'][0]['name'],
                'Image': x['track']['album']['images']}
    track_list.append(new_dict)
print(track_list)

str = ""
for x in track_list:
    str += '"' + x['Name'] + '"'
    str += '"' + x['Artist'] + '"'

print(str)