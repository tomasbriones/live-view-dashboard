import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
LOCALHOST = os.getenv("LOCALHOST")
API_PORT = os.getenv("API_PORT")
API_URL = os.getenv("API_URL")
SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = os.getenv("SSH_PORT")
SSH_PK = os.getenv("SSH_PK")
SSH_USER = os.getenv("SSH_USER")
SSH_PWD = os.getenv("SSH_PWD")
# ENVIRONMENT = os.getenv("ENVIRONMENT")
