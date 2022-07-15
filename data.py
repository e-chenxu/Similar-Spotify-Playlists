import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

# my keys
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


# this will get a list of track and their data in a dictionary
def get_tracks_from_pl(pl_link) -> list:
    # get playlist id
   # playlist_link = "https://open.spotify.com/playlist/4YXr1VsIVKxOk5xYrZxGlT"
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


# gets name of playlist
def get_playlist_name(pl_link) -> str:
    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist(playlist_id)
    items = results
    return items['name']


# gets link of playlist image
def get_playlist_art(pl_link) -> str:
    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist(playlist_id)
    items = results
    return items['images'][0]['url']


def find_similar_playlists(track_list) -> list:
    # we have to first create a string that contains all the track names plus artists in quotes
    total_string = ""
    for x in track_list:
        total_string += '"' + x['Name'] + '"'
        total_string += '"' + x['Artist'] + '"'
    return get_google_results(total_string)


# google search data functions

# gets source code from link
def get_source_code(link):
    try:
        session = HTMLSession()
        source = session.get(link)
        return source
    except requests.exceptions.RequestException as e:
        print(e)


# gets page of playlists
def get_google_results(query):
    query = urllib.parse.quote_plus(query)
    response = get_source_code("https://www.google.com/search?q==site%3Aopen.spotify.com+" + query)

    # table of any google links
    results = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.')

    # remove google urls
    for url in results[:]:
        if url.startswith(google_domains):
            results.remove(url)

    return results