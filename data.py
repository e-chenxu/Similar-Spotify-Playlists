import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import urllib
import pandas as pd
import random
from requests_html import HTML
from requests_html import HTMLSession

# my keys
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


# this function will try to find 5 different playlists
def get_five_playlists(track_list) -> list:
    # total playlist list that we are returning
    playlist_list = set()
    i = 0
    while i < 5:
        # THIS SHOULD BE CHANGED LATER
        # first we get 2 random songs from the track_list
        random_sample = random.sample(track_list, 2)

        # we then find similar playlists using these random samples
        temp_playlist = find_similar_playlists(random_sample)

        # append items to the playlist list but make sure to break when its mroe or less than 5
        for item in temp_playlist:
            # make sure correct link
            if not correct_link_check(item):
                continue
            # make sure no duplicates
            playlist_list.add(item)
            if len(playlist_list) >= 5:
                break

        # if not 5, then loop again
        if len(playlist_list) >= 5:
            break
        # make sure no duplicates (turn into set, then list)
        i += 1
    # NOW THAT THERE IS NO DUPLICATES, WE CAN RETURN A LIST OF STATS
    actual_playlist_list = []
    for x in playlist_list:
        new_dict = {'Name': get_playlist_name(x),
                    'Image': get_playlist_art(x),
                    'Link': x}
        actual_playlist_list.append(new_dict)
    return actual_playlist_list


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
        # if image for album doesnt exist, skip because not a song
        if not x['track']['album']['images']:
            continue
        new_dict = {'Name': x['track']['name'],
                    'Artist': x['track']['artists'][0]['name'],
                    'Image': x['track']['album']['images'][2]['url']}
        track_list.append(new_dict)
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


def find_similar_playlists(track_list) -> set:
    # we have to first create a string that contains all the track names plus artists in quotes
    total_string = ""
    for x in track_list:
        total_string += '"' + x['Name'] + '"'
        total_string += '"' + x['Artist'] + '"'
    return set(get_google_results(total_string))


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


def correct_link_check(link):
    if "open.spotify.com/playlist/" in link:
        return True
    else:
        return False
