from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import config

SQLALCHEMY_DATABASE_URL = f"mariadb+mariadbconnector://{config.MYSQL_USER}:{config.MYSQL_PASS}@{config.MYSQL_IP}:{config.MYSQL_PORT}/{config.MYSQL_DB}"

# print("Database URL is ",SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
