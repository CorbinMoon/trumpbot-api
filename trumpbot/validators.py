import re


def validate_password(password):
    if password is None:
        return False
    if len(password) < 10:
        return False
    return True

def validate_username(username):
    if username is None:
        return False
    if len(username) < 8 or len(username) > 25:
        return False
    if not re.match('[a-zA-Z0-9]+', username):
        return False
