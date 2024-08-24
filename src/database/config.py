

CONNECTOR  = "mariadb+mariadbconnector"
MYSQL_USER = "local"
MYSQL_PASS = "local"
MYSQL_IP   = "db"
MYSQL_PORT = "3306"
MYSQL_DB   = "ekpedeutikoi"

ECHO_QUERIES = False

SQLALCHEMY_DATABASE_URL = f"{CONNECTOR}://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_IP}:{MYSQL_PORT}/{MYSQL_DB}"

print(f"Database URL is {SQLALCHEMY_DATABASE_URL}")
