# def get_movie_by_title(input_title):
#     parameters = {'t': input_title, 'r': 'json', 'plot': 'full', 'Page': 2}
#     data_url = 'http://www.omdbapi.com/?apikey=' + API_KEY
#     data = requests.get(data_url, params=parameters).json()
#
#     poster = data['Poster']
#     imdb_rating = data['imdbRating']
#     title = data['Title']
#
#     return {'poster': poster, 'imdb_rating': imdb_rating, 'title': title}
#
#
# @app.route('/', method=['GET', 'POST'])
# def search():
#     data = request.data
#     print(get_movie_by_title(data))
#     python_data = json.loads(data)
#     out_data = {
#         "hello": "hepp",
#         "value": 45
#     }
#     response = app.response_class(
#         response=json.dumps(out_data),
#         status=200,
#         mimetype='application/json'
#     )
#     return response
