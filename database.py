import psycopg2

def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="project18_db",
        user="yashwanirao",
        password=""
    )
    return connection