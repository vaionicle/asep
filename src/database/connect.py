from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import MYSQL_DB, MYSQL_IP, MYSQL_PORT, MYSQL_PASS, MYSQL_USER

SQLALCHEMY_DATABASE_URL = f"mariadb+mariadbconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_IP}:{MYSQL_PORT}/{MYSQL_DB}"

print("Database URL is ",SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
