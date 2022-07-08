import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# my keys
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


# this will get a list of track and their data in a dictionary
def getTracksFromPlaylist(pl_link) -> list:
    # get playlist id
    playlist_link = "https://open.spotify.com/playlist/4YXr1VsIVKxOk5xYrZxGlT"
    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    # continue if there is more items
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    # create an list and append the track name, artist, and picture
    track_list = []
    for x in tracks:
        new_dict = {'Name': x['track']['name'],
                    'Artist': x['track']['artists'][0]['name'],
                    'Image': x['track']['album']['images'][2]['url']}
        track_list.append(new_dict)
    print(track_list)
    return track_list



def searchTracks(tracks):
    return