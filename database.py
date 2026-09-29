import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

DATABASE_CONFIG = {
    "host": "localhost",
    "database": "project18_db",
    "user": "yashwanirao",
    "port": 5432
}


def get_connection():

    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)

    return psycopg2.connect(
        host=DATABASE_CONFIG["host"],
        database=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        port=DATABASE_CONFIG["port"]
    )