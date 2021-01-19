import json

from flask_login import login_required, current_user
from flask_security.utils import login_user, logout_user, verify_password
from flask_security import roles_required
from flask import render_template, request, redirect, url_for, flash


from controllers.role_controller import get_all_roles, get_role_by_name
from controllers.user_controller import create_user, get_all_users, \
    get_user_by_username, get_user_by_email, add_role_to_user

from views.utils.flask_wtf_classes import RegisterForm, LoginForm
from views import app


@app.route("/")
def index():
#     user = get_user_by_email("marcus.eriksson00@hotmail.com")
#     role = get_role_by_name("editor")
#     add_role_to_user(user, role)
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == "POST":
        create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
            username=form.username.data
        )

        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', first_name=current_user.first_name, roles=current_user.roles)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_email(email=form.email.data)
        if user and verify_password(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            flash('Wrong email or password')
            return redirect('signin')

    return render_template('signin.html', form=form)

@app.route("/signout")
def signout():
    logout_user()
    return render_template('index.html')


@app.route('/edit_account')
def edit_account():
    return render_template('edit_account.html')


@app.route('/friends')
def friends():
    return render_template("friends.html")


@app.errorhandler(404)
def handler404(_):
    return render_template('404.html')


@app.route("/admin")
@roles_required("admin")
def admin():
    return render_template('admin.html', users=get_all_users(), roles=get_all_roles())


@app.route("/admin/users/<username>")
@roles_required("admin")
def user(username):
    return render_template('user.html', user=get_user_by_username(username))


@app.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html', watchlist=current_user.watchlist)

# @app.route('/movies/<title>')
# def movie(title):
#     movie_information = get_movie_by_title_first(title)
#     return render_template('movie.html', movie_information=movie_information)
