from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from flask_security import roles_required
from flask_security.utils import login_user, logout_user, verify_password

from controllers.chat_controller import remove_user_chats
from controllers.role_controller import add_admin_role_to_user, create_role
from controllers.user_controller import create_user, get_all_users, get_user_by_username, get_user_by_email, \
    add_profile_picture_to_user, delete_profile_picture_if_exists, remove_user as ru

from views import app
from views.utils.flask_wtf_classes import RegisterForm, LoginForm

index = Blueprint('index', __name__, url_prefix='/')


@index.route("/", methods = ['GET'])
def _index():
    login_form = LoginForm()
    return render_template("index.html", login_form=login_form)


@index.route("/", methods=['POST'])
def sign_in():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = get_user_by_email(email=login_form.email.data)
        if user and verify_password(login_form.password.data, user.password):
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('profile'))
        else:
            return render_template("index.html", login_form=login_form, errors="Wrong email or password")


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    errors = []
    if request.method == "POST":

        if get_user_by_email(form.email.data):
            errors.append("Email is already in use")

        if get_user_by_username(form.username.data):
            errors.append("Username is already taken")

        if form.validate_on_submit() and len(errors) == 0:
            create_user(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                username=form.username.data
            )
            return redirect(url_for('index.sign_in'))

    return render_template('signup.html', register_form=form, errors=errors)


@app.route("/signout")
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('index._index'))


@app.route('/users/<username>', methods=['GET'])
@login_required
def remove_user(username):
    user = get_user_by_username(username)
    ru(user)
    remove_user_chats(user)
    return redirect(url_for('index._index'))


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


@app.route('/profile', methods=['POST'])
@login_required
def post_profile_picture():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if not file.filename:
        flash('No selected file')
        return redirect(request.url)

    if file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
        delete_profile_picture_if_exists(current_user)
        add_profile_picture_to_user(current_user, file)
    else:
        flash('Wrong file format. Choose between png, jpg, jpeg and gif.')

    return redirect(url_for('profile'))


@app.route('/watchlist', methods=['GET'])
@login_required
def watchlist():
    return render_template('watchlist.html')


@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    return render_template("friends.html", user=current_user, friends=current_user.friends)


@app.route('/friends/<username>', methods=['GET', 'POST'])
@login_required
def friend(username):
    return render_template("friend.html", user=current_user, friend=get_user_by_username(username))


@app.route("/admin", methods=['GET'])
@roles_required("admin")
def admin():
    return render_template('admin.html', users=get_all_users())


@app.route("/admin/users/<username>", methods=['GET'])
@roles_required("admin")
def user(username):
    return render_template('user.html', user=get_user_by_username(username))


@app.errorhandler(404)
def handler404(e):
    return render_template('404.html', error=e)