import string
import random
from controllers.user_controller import create_user


def get_random_password():
    characters = string.ascii_lowercase + "0123456789" + "@.,?"
    return ''.join(random.choice(characters) for i in range(13))


def get_random_chars():
    alphabet = string.ascii_lowercase
    return ''.join(random.choice(alphabet) for i in range(13))


def get_random_email():
    return f'{get_random_chars()}@{get_random_chars()}.com'


def create_test_user():
    return create_user(
        first_name=get_random_chars(),
        last_name=get_random_chars(),
        email=get_random_chars(),
        password=get_random_password(),
        username=get_random_chars(),
    )