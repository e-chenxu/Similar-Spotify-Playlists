import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import data

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# results = sp.search(q='weezer', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#   print(idx, track['name'])
playlist_link = "https://open.spotify.com/playlist/4YXr1VsIVKxOk5xYrZxGlT"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
results = sp.playlist_items(playlist_URI)
tracks = results['items']
# while results['next']:
#   results = sp.next(results)
#   tracks.extend(results['items'])

# track_list = []
# for x in tracks:
#    new_dict = {'Name': x['track']['name'], 'Artist': x['track']['artists'][0]['name'],
#               'Image': x['track']['album']['images']}
#   track_list.append(new_dict)
print(data.get_track_ids_from_pl("https://open.spotify.com/playlist/37i9dQZF1E8MbeBoZEFkA4"))


# gets number of song matches of 2 playlists
# get both track lists
track_list = data.get_track_ids_from_pl("https://open.spotify.com/playlist/0NTOWk1KxteInzI85BNEjB")
track_list_og = data.get_track_ids_from_pl("https://open.spotify.com/playlist/37i9dQZF1E8MbeBoZEFkA4")
a = set(track_list).intersection(track_list_og)
b = len(a)
print(len(a))



# str = ""
# for x in track_list:
#    str += '"' + x['Name'] + '"'
#    str += '"' + x['Artist'] + '"'

# print(str)
