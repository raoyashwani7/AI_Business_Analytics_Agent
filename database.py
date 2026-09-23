import psycopg2


DATABASE_CONFIG = {
    "host": "localhost",
    "database": "project18_db",
    "user": "yashwanirao",
    "port": 5432
}


def get_connection():
    connection = psycopg2.connect(
        host=DATABASE_CONFIG["host"],
        database=DATABASE_CONFIG["database"],
        user=DATABASE_CONFIG["user"],
        port=DATABASE_CONFIG["port"]
    )

    return connection