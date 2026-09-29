from langchain_core.tools import tool
from database import get_connection


@tool
def query_database(sql: str) -> str:
    """
    Execute a SQL query on the PostgreSQL business database.
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql)
        rows = cursor.fetchmany(20)

        cursor.close()
        connection.close()

        if not rows:
            return "No data found."

        result = "\n".join(
            str(tuple(row))
            for row in rows
        )

        if len(result) > 4000:
            result = result[:4000] + "\n...[result truncated]"

        return result

    except Exception as e:
        return f"Database error: {str(e)}"