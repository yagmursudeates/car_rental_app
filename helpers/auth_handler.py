from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Hashes a password using Werkzeug's generate_password_hash.
    """
    return generate_password_hash(password, method='pbkdf2')

def check_password(hashed_password, password):
    """
    Verifies a password against its hashed version.
    """
    return check_password_hash(hashed_password, password)

def is_authenticated(session):
    """
    Checks if the user is authenticated by verifying the session.
    """
    return 'user_id' in session

def get_current_user(session, UserModel):
    """
    Fetches the currently logged-in user from the session.
    """
    if 'user_id' in session:
        return UserModel.query.get(session['user_id'])
    return None