import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# my keys
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="b4129b58122543428ebab649da44221f",
                                                           client_secret="a46d14a8794643d982374c80533b837d"))


# this will get a list of track and their data in a dictionary
def getTracksFromPlaylist(pl_link):

    return



def searchTracks(tracks):
    return