from flask import request
from flask_login import current_user, login_required

import json

from data.MongoDB_MongoEngine.models.messages import Message

from controllers.chat_controller import initiate_chat, get_all_chats, add_message_to_chat, get_chat_between_users, get_chat_by_id
from controllers.omdb_controller import get_movies_by_title, get_movie_by_imdb_id
from controllers.role_controller import get_role_by_name, delete_admin_role_from_user
from controllers.user_controller import add_movie_to_users_watchlist, get_user_by_email, add_role_to_user, \
    add_friendship, delete_movie_from_users_watchlist, get_user_by_username, get_all_friends

from views import app


@app.route('/api/search', methods=['POST'])
def post_search():
    search_term = request.values['search_term']

    response = app.response_class(
        response=json.dumps(get_movies_by_title(search_term)),
        status=200,
        mimetype="application/json"
    )

    return response


@app.route('/api/movies/movie', methods=['POST'])
def get_movie():
    imdb_id = request.values['imdb_id']
    response = app.response_class(
        response=get_movie_by_imdb_id(imdb_id),
        status=200,
        mimetype="application/json"
    )

    return response


@app.route('/api/users/<username>/watchlist', methods=['POST'])
@login_required
def post_watchlist(username):
    movie = json.loads(request.values['movie'])

    if movie in current_user.watchlist:
        resp = f"Already added {movie['Title']} to your watchlist"
    else:
        add_movie_to_users_watchlist(current_user, movie)
        resp = f"{movie['Title']} added"

    response = app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/watchlist', methods=['GET'])
@login_required
def get_watchlist(username):
    watchlist = current_user.watchlist
    print(watchlist)
    response = app.response_class(
        response=json.dumps(watchlist),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/watchlist', methods=['DELETE'])
@login_required
def delete_from_watchlist(username):
    movie = json.loads(request.values['movie'])
    resp = ""
    delete_movie_from_users_watchlist(current_user, movie)

    if movie not in current_user.watchlist:
        resp = f"You removed {movie['Title']} to your watchlist"
    else:
        resp = f"You failed to remove {movie['Title']} to your watchlist"

    response = app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/friends', methods=['GET'])
@login_required
def get_friends(username):
    friends = get_all_friends(current_user)
    response = app.response_class(
        response=json.dumps(friends),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/friends', methods=['POST'])
@login_required
def post_friendship(username):
    found_friend = get_user_by_username(request.values['username'])
    logged_in_user = get_user_by_username(current_user.username)

    if found_friend:
        if found_friend in logged_in_user.friends:
            resp = f"you are already friend with {found_friend.username}"
        else:
            add_friendship(user=logged_in_user, friend=found_friend)
            resp = f"You are now friends with {found_friend.username}"
            initiate_chat(user_1=logged_in_user, user_2=found_friend)
    else:
        resp = f"Found no user with username {request.values['username']}"

    response = app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype="application/json"
    )

    return response


@app.route('/api/users/<username>/friends/chats', methods=['GET'])
@login_required
def get_chat(username):
    friend = get_user_by_username(request.values['friend'])
    chat = get_chat_between_users(current_user, friend)
    print(chat.members)
    response = app.response_class(
        response=json.dumps(chat.to_json()),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/friends/user_name_for_friend/chat', methods=['POST'])
@login_required
def post_message(username):
    chat = get_chat_by_id(request.values['chat'])
    message = Message(sent_by=get_user_by_username(request.values['sent_by']), text=request.values['message'])
    add_message_to_chat(chat, message)
    response = app.response_class(
        response=json.dumps("sent"),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/roles', methods=['POST'])
@login_required
def add_role(username):
    user = get_user_by_username(json.loads(request.values['username']))
    admin_role = get_role_by_name("admin")
    add_role_to_user(user=user, role=admin_role)
    resp = f"added role"
    response = app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/roles', methods=['DELETE'])
@login_required
def delete_role(username):
    user = get_user_by_username(json.loads(request.values['username']))
    delete_admin_role_from_user(user)
    resp = f"removed role"
    response = app.response_class(
        response=json.dumps(resp),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/roles/admin', methods=['GET'])
@login_required
def get_if_admin_role(username):
    user = get_user_by_username(json.loads(request.values['username']))

    response = app.response_class(
        response=json.dumps(True if len(user.roles) > 0 else False),
        status=200,
        mimetype="application/json"
    )
    return response


@app.route('/api/users/<username>/profile_picture', methods=['GET'])
@login_required
def get_profile_picture(username):
    # TODO: add check if picture do not exist
    response = current_user.profile_picture.read()

    response = app.response_class(
        response=response,
        status=200,
    )

    return response

