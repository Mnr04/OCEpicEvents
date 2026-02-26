import bcrypt
import re
from datetime import datetime

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_bytes.decode('utf-8')

def verify_password(plain_password, hashed_password):
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r"^\+?[0-9\s\-]{8,15}$"
    return re.match(pattern, phone) is not None

def validate_amount(amount):
    try:
        val = float(amount)
        return val >= 0
    except ValueError:
        return False

def validate_dates(start_date_str, end_date_str):
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
        end = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
        return end > start
    except ValueError:
        return False