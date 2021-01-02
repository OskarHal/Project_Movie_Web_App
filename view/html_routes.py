from view import app
from flask import render_template, session


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login/<username>')
def login(username):
    session['username'] = username
    return render_template('index.html')


@app.route("/logout")
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/profile')
def profile():
    username = session['username']
    if username is None:
        return render_template('index.html')
    return render_template('profile.html', username=username)


@app.route('/friends')
def friends():
    return render_template("friends.html")


@app.errorhandler(404)
def handler404(_):
    return render_template('404.html')


