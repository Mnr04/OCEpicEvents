import bcrypt

def hash_password(password: str) -> str:

    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_password, salt)

    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:

    bytes_plain = plain_password.encode('utf-8')
    bytes_hashed = hashed_password.encode('utf-8')

    return bcrypt.checkpw(bytes_plain, bytes_hashed)