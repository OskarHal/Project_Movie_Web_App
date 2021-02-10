import requests

from data.omdb.api_settings import API_KEY


def get_movies_by_title(input_title):
    parameters = {'s': {input_title}, 'r': 'json', 'plot': 'short', 'page': 1, 'apikey': API_KEY}
    return [movie for movie in requests.get(f'http://www.omdbapi.com/', params=parameters).json()['Search']]


def get_movie_by_title_first(input_title):
    parameters = {'t': input_title, 'r': 'json', 'plot': 'short', 'apikey': API_KEY}

    return requests.get(f'http://www.omdbapi.com/', params=parameters)


def get_movie_by_imdb_id(imdb_id):
    parameters = {'i': imdb_id, 'r': 'json', 'plot': 'short', 'apikey': API_KEY}

    return requests.get(f'http://www.omdbapi.com/', params=parameters).content.decode('utf-8')
