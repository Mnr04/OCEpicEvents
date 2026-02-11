import jwt
from models.models import User
import datetime
from database import SessionLocal
from utils import verify_password

SECRET_KEY = "k&1$v18#50$E^4!k5$"
ALGORITHM = "HS256"

def login_user(username, password):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if not user or not verify_password(password, user.password_hash):
        return None

    payload = {
        "user_id": user.id,
        "role": user.role.value,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


