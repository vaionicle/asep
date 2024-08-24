from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import SQLALCHEMY_DATABASE_URL, ECHO_QUERIES

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=ECHO_QUERIES)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
