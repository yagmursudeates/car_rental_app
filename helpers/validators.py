import re

def is_valid_email(email):
    """
    Validates an email address using a regex.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    """
    Validates a password with the following rules:
    - At least 8 characters
    - At least 1 number
    - At least 1 special character
    """
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):  # At least 1 number
        return False
    if not re.search(r'[^\w]', password):  # At least 1 special character
        return False
    return True

def validate_user_registration(data):
    """
    Validates registration form data.
    """
    errors = {}
    if not is_valid_email(data.get('email', '')):
        errors['email'] = "Invalid email format."
    if not is_valid_password(data.get('password', '')):
        errors['password'] = "Password must be at least 8 characters long, include 1 number and 1 special character."
    if data.get('password') != data.get('confirm_password'):
        errors['confirm_password'] = "Passwords do not match."
    return errors