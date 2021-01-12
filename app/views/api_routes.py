import requests
from views.api_settings import API_KEY


def get_movie_by_title(input_title):
    parameters = {'s': input_title, 'r': 'json', 'plot': 'short'}
    req = requests.get(f'http://www.omdbapi.com/?apikey={API_KEY}', params=parameters)
    print(req.json())
    return req.json()