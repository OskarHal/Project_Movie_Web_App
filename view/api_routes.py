from flask import request


def get_movie_by_title(input_title):
    parameters = {'t': input_title, 'r': 'json', 'plot': 'short'}
    api_key = ''
    req = request.get(data_URL='http://www.omdbapi.com/?apikey=' + api_key, params=parameters)



    result = req.json()

    print(result)


#get_movie_by_title("Interstellar")

# http://www.omdbapi.com/?i=tt3896198&apikey=6f91aff9