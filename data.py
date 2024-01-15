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
    playlist_list = set()  # make sure no duplicates
    song_find_count = 3  # initially, find playlists with a random sample of 3 songs
    i = 0
    searches = 3 + 2 * int(search_algo)

    # adjust sample if the track list is too small
    if len(track_list) < song_find_count:
        song_find_count = 1

    while i < searches:
        random_sample = random.sample(track_list, song_find_count)
        temp_playlist = find_similar_playlists(random_sample)

        # append items to the playlist list but only add max of 3 each sample for variety
        added_items = 0
        for item in temp_playlist:
            # remove false links and duplicates
            if not correct_link_check(item) or item == spotify_link:
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
    track_list_original = get_track_ids_from_pl(spotify_link)
    for x in playlist_list:
        new_dict = get_playlist_info(x, track_list_original)
        # check if too many tracks
        if new_dict['Count'] > 300:
            continue
        # did not get similar tracks from other
        if new_dict['Count'] > 100:
            new_dict['Similar'] = get_song_matches(x, track_list_original)
        actual_playlist_list.append(new_dict)

    new_list = sorted(actual_playlist_list, key=lambda a: int(a['Similar']), reverse=True)
    return new_list


def get_tracks_from_pl(pl_link) -> list:
    """Grab a list containing dictionaries of track data of name,
    artist, image
    """

    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    # continue if there is more items because spotipy tries to stop at 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # create a list and append the track name, artist, and picture
    track_list = []
    for x in tracks:
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


def get_track_ids_from_pl(pl_link) -> set:
    """Grab a list containing only the name + artist of the
    tracks as an ID
    example:
    Despacito Luis Fonsi
    """

    playlist_id = pl_link.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    # continue if there is more items because spotipy tries to stop at 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    track_id_set = set()
    for x in tracks:
        if x['track'] is None:
            continue
        total_track = x['track']['name'] + ' ' + x['track']['artists'][0]['name']
        track_id_set.add(total_track)
    return track_id_set


def get_playlist_info(pl_link, track_list_original=None) -> dict:
    """Grab all info for 1 playlist in a dictionary
    Name - name of playlist
    Image - url for playlist image
    Desc - playlist description
    Count - number of tracks
    Link - playlist link
    """

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

    # spotipy limits songs over 100, so we can save time by calculating similar songs early
    if new_dict['Count'] <= 100 and track_list_original is not None:
        tracks = results['tracks']['items']

        track_id_set = set()

        for x in tracks:
            if x['track'] is None:
                continue
            total_track = x['track']['name'] + ' ' + x['track']['artists'][0]['name']
            track_id_set.add(total_track)

        new_dict['Similar'] = str(len(track_id_set.intersection(track_list_original)))

    return new_dict


def get_song_matches(pl_link, track_list_og) -> str:
    """Find how many songs are similar in
    comparison to your playlist using the
    track IDs
    """

    track_list = get_track_ids_from_pl(pl_link)
    return str(len(track_list.intersection(track_list_og)))


def find_similar_playlists(track_list) -> set:
    # we have to first create a string that contains all the track names plus artists in quotes
    total_string = ""
    for x in track_list:
        total_string += '"' + x['Name'] + '"'
        total_string += '"' + x['Artist'] + '"'
    found_playlists = get_google_results(total_string)
    random.shuffle(found_playlists)
    return set(found_playlists)


def fix_text(text) -> str:
    html_text = html.unescape(text)
    return TAG_RE.sub('', html_text)


# Google and link search data functions #


def get_source_code(link):
    try:
        session = HTMLSession()
        html_source = session.get(link)
        return html_source
    except requests.exceptions.RequestException as e:
        print(e)


# gets page of playlists
def get_google_results(query):
    """Using a query, Google search and return all link results"""

    query = urllib.parse.quote_plus(query)
    response = get_source_code("https://www.google.com/search?q==site%3Aopen.spotify.com%2Fplaylist+" + query)
    if not response:
        return []

    results = list(response.html.absolute_links)
    wanted_domains = ('https://www.google.com/url?esrc=s&q=&rct=j&sa=U&url=https://open.spotify.com/playlist')

    new_results = []
    # remove every url except spotify playlists
    for url in results[:]:
        if url.startswith(wanted_domains):
            new_url = url.replace('https://www.google.com/url?esrc=s&q=&rct=j&sa=U&url=', '')
            list_url = new_url.split('&')
            new_url = list_url[0]
            new_results.append(new_url)
    print(new_results)
    return new_results


def correct_link_check(link):
    if "open.spotify.com/playlist/" in link:
        return True
    else:
        return False
