import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import urllib
import random
from requests_html import HTML
from requests_html import HTMLSession
import sys

# my keys
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


# this function will try to find 5 different playlists
def get_five_playlists(spotify_link) -> list:
    # get the track list from this spotify link
    track_list = get_tracks_from_pl(spotify_link)
    # total playlist list that we are returning
    playlist_list = set()
    i = 0
    # find playlists with this number of songs
    song_find_count = 3
    # playlist finding algorithm

    while i < 5:
        # THIS SHOULD BE CHANGED LATER
        # first we get a variable amoutn of random songs from the track_list

        # if the track list is too small, then we have to adjust the find count
        if len(track_list) < song_find_count:
            song_find_count = len(track_list)

        # always find at least 1, make sure the length is more than 0, also find 1 at end
        if i == 4 or (song_find_count < 1 and len(track_list) > 0):
            song_find_count = 1

        random_sample = random.sample(track_list, song_find_count)

        # we then find similar playlists using these random samples
        temp_playlist = find_similar_playlists(random_sample)
        print(temp_playlist, file=sys.stdout)

        # append items to the playlist list but make sure to break when its mroe or less than 10
        added_items = 0
        for item in temp_playlist:
            # dont add too much
            if len(track_list) > song_find_count and song_find_count < 3 and added_items >= 2:
                break
            # make sure correct link
            if not correct_link_check(item):
                continue
            # make sure no duplicates
            playlist_list.add(item)
            added_items += 1
            # no more than 10 tracks (testing purposes)
            if len(playlist_list) >= 10:
                break

        # if not 10, then loop again
        if len(playlist_list) >= 10:
            break
        # make sure no duplicates (turn into set, then list)
        i += 1

        # find 3 for first 2 iterations, then 2 after
        if i == 2:
            song_find_count = 2

    # NOW THAT THERE IS NO DUPLICATES, WE CAN RETURN A LIST OF STATS
    actual_playlist_list = []
    for x in playlist_list:
        new_dict = get_playlist_info(x)
        new_dict['Similar'] = get_song_matches(x, spotify_link)
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


# this will get a list of track ids
def get_track_ids_from_pl(pl_link) -> list:
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
    track_id_list = []
    for x in tracks:
        # if image for album doesnt exist, skip because not a song
        if not x['track']['album']['images']:
            continue
        track_id_list.append(x['track']['id'])
    return track_id_list


# gets all playlist info for 1 playlist into a dictionary
def get_playlist_info(pl_link) -> dict:
    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist(playlist_id)
    new_dict = {'Name': results['name'],
                'Image': results['images'][0]['url'],
                'Desc': results['description'],
                'Count': results['tracks']['total'],
                'Link': pl_link}
    return new_dict


# gets number of song matches of 2 playlists
def get_song_matches(pl_link, pl_link_og) -> str:
    # get both track lists
    track_list = get_track_ids_from_pl(pl_link)
    track_list_og = get_track_ids_from_pl(pl_link_og)
    # get the set of the same ids, then get the length
    return str(len(set(track_list).intersection(track_list_og)))


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
    response = get_source_code("https://www.google.com/search?q==site%3Aopen.spotify.com%2Fplaylist+" + query)

    # table of any google links
    results = list(response.html.absolute_links)
    print(results, file=sys.stdout)

    wanted_domains = ('https://open.spotify.com/playlist')

    # remove every url except spotify playlists
    for url in results[:]:
        if url.startswith(wanted_domains):
            continue
        else:
            results.remove(url)

    return results


def correct_link_check(link):
    if "open.spotify.com/playlist/" in link:
        return True
    else:
        return False
