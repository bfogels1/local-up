
# TODO define a more serious password validation rule
# (e.g. at least X uppercase or symbols, etc.)
def password_is_valid(password):
    if password is None or len(password) < 5:
        return False
    return True
