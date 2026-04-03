from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM

# setup bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashing password before store in DB


def hash_password(password: str):
    password = password.encode("utf-8")[:72].decode("utf-8", "ignore")
    return pwd_context.hash(password)

# verify password with hashed password


def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password.encode(
        "utf-8")[:72].decode("utf-8", "ignore")
    return pwd_context.verify(plain_password, hashed_password)

# create access token - 30 min


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# create refresh token - 7 days


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
