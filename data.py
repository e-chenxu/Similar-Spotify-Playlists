import html
import re
import spotipy
import requests
import urllib
import random
from spotipy.oauth2 import SpotifyClientCredentials
from requests_html import HTMLSession

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# removing unneeded tags
TAG_RE = re.compile(r'<[^>]+>')


def get_playlists(spotify_link, search_algo) -> list:
    """ Try to return at most 15 playlists and info by searching Google
    and getting Spotify data, will use the search_algo variable
    to determine how exhaustive the search algorithm will be
    """
    track_list = get_tracks_from_pl(spotify_link)
    playlist_list = set()             # make sure no duplicates
    song_find_count = 3               # initially, find playlists with a random sample of 3 songs
    i = 0
    searches = 3 + 2*int(search_algo)

    # adjust sample if the track list is too small
    if len(track_list) < song_find_count:
        song_find_count = 1

    while i < searches:
        random_sample = random.sample(track_list, song_find_count)
        temp_playlist = find_similar_playlists(random_sample)

        # append items to the playlist list but only add max of 3 each sample for variety
        added_items = 0
        for item in temp_playlist:
            if not correct_link_check(item):
                continue
            playlist_list.add(item)
            added_items += 1
            if len(playlist_list) >= 15 or (added_items > 2 and len(track_list) > song_find_count):
                break

        if len(playlist_list) >= 15:
            break

        # search algorithm
        if i == searches // 3:
            song_find_count = 2
        elif i == searches - (searches // 5):
            song_find_count = 1
        i += 1

    # return a list of playlists and respective info
    actual_playlist_list = []
    for x in playlist_list:
        new_dict = get_playlist_info(x)
        # check if too many tracks
        if new_dict['Count'] > 250:
            continue
        new_dict['Similar'] = get_song_matches(x, spotify_link)
        actual_playlist_list.append(new_dict)

    new_list = sorted(actual_playlist_list, key=lambda a: int(a['Similar']), reverse=True)
    return new_list


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
        if x['track'] is None:
            continue
        if len(x['track']['album']['images']) == 0:
            image_results = ''
        else:
            image_results = x['track']['album']['images'][2]['url']
        new_dict = {'Name': x['track']['name'],
                    'Artist': x['track']['artists'][0]['name'],
                    'Image': image_results}
        track_list.append(new_dict)
    return track_list


# this will get a list of track ids
def get_track_ids_from_pl(pl_link) -> set:
    # get playlist id
    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    # continue if there is more items
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    # create an set and append the track name, artist, and picture
    track_id_set = set()
    # ADD NAME OF SONG AND ARTIST ON SAME LINE
    for x in tracks:
        # if image for album doesnt exist, skip because not a song
        if x['track'] is None:
            continue
        total_track = x['track']['name'] + ' ' + x['track']['artists'][0]['name']
        track_id_set.add(total_track)
    return track_id_set


# gets all playlist info for 1 playlist into a dictionary
def get_playlist_info(pl_link) -> dict:
    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist(playlist_id)
    if len(results['images']) == 0:
        image_results = ''
    else:
        image_results = results['images'][0]['url']
    new_dict = {'Name': results['name'],
                'Image': image_results,
                'Desc': fix_text(results['description']),
                'Count': results['tracks']['total'],
                'Link': pl_link}
    return new_dict


# gets number of song matches of 2 playlists
def get_song_matches(pl_link, pl_link_og) -> str:
    # get both track lists
    track_list = get_track_ids_from_pl(pl_link)
    track_list_og = get_track_ids_from_pl(pl_link_og)
    # get the set of the same ids, then get the length
    return str(len(track_list.intersection(track_list_og)))


def find_similar_playlists(track_list) -> set:
    # we have to first create a string that contains all the track names plus artists in quotes
    total_string = ""
    for x in track_list:
        total_string += '"' + x['Name'] + '"'
        total_string += '"' + x['Artist'] + '"'
    # shuffle this set
    found_playlists = get_google_results(total_string)
    random.shuffle(found_playlists)
    # get rid of duplicates
    return set(found_playlists)


def fix_text(text) -> str:
    html_text = html.unescape(text)
    return TAG_RE.sub('', html_text)


# BREAK #

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
