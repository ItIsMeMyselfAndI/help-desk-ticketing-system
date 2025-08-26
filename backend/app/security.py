import bcrypt

def hash_password(plain_password: str) -> str:
    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = bcrypt.hashpw(plain_bytes, bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_bytes, hashed_bytes)
