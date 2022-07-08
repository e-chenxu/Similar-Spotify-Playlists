import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession


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


print(get_google_results('''"Paralyzer""Finger Eleven""Apologize""grandson"'''))
