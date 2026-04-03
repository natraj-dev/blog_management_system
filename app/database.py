from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# load env variable from .env file
load_dotenv()

# get database_url from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# create db engine connect to DB
engine = create_engine(DATABASE_URL)

# session class for interact with DB [CRUD]
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
