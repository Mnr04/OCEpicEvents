import jwt
from models.models import User
import datetime
from database import Session
from utils import verify_password
import os

SECRET_KEY = "k&1$v1k&1$v18#50$E^4!k5$8#50$E^4!k5$k&1$v18#50$E^4!k5$"
ALGORITHM = "HS256"
TOKEN_FILE = "session_token.txt"

def login_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not user or not verify_password(password, user.password_hash):
        return None

    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role.value,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    with open(TOKEN_FILE, "w") as f:
        f.write(token)

    return token


def get_logged_user():
    if not os.path.exists(TOKEN_FILE):
        return None

    try:
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        print("Session expirée.")
        return None
    except jwt.InvalidTokenError:
        print("Token invalide.")
        return None



