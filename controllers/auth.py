import jwt
from models.models import User
import datetime
from database import Session
from utils import verify_password
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_FILE = "session_token.txt"

def login_user(username, password):
    """
    Check the username and password.
    If correct, create a JWT token, save it in a file, and return it.
    """
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not user or not verify_password(password, user.password_hash):
        return None

    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role.value,
        # Token expiration is set to 4 hours for security reasons (OWASP recommendation)
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    with open(TOKEN_FILE, "w") as f:
        f.write(token)

    return token


def get_logged_user():
    """
    Read the token from the file and decode it.
    Return the user data if the token is valid, or None if expired/invalid.
    """
    if not os.path.exists(TOKEN_FILE):
        return None

    try:
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def logout_user():
    """
    Delete the token file to disconnect the user.
    """
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        return True
    return False