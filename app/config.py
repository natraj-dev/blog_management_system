import os
from dotenv import load_dotenv

load_dotenv()

# get secret key from .env for jwt token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
