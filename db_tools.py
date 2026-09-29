from langchain_core.tools import tool
from database import get_connection


@tool
def query_database(sql: str) -> str:
    """
    Execute a SQL query on the PostgreSQL business database.

    Use this tool when the user asks a question that requires
    business data.
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        if not rows:
            return "No data found."

        return "\n".join(
            str(tuple(row))
            for row in rows
        )

    except Exception as e:
        return f"Database error: {str(e)}"