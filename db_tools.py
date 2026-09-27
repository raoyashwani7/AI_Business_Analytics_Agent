from langchain_core.tools import tool
from database import run_query


@tool
def query_database(sql: str) -> str:
    """
    Execute a SQL query on the PostgreSQL business database.
    Use this tool when the user asks a question that requires
    business data.
    """

    try:
        rows = run_query(sql)

        if not rows:
            return "No data found."

        return "\n".join(
            str(tuple(row))
            for row in rows
        )

    except Exception as e:
        return f"Database error: {str(e)}"

from langchain_core.tools import tool
from database import run_query


@tool
def query_database(sql: str) -> str:
    """
    Execute a SQL query on the PostgreSQL business database.
    Use this tool when the user asks a question that requires
    business data.
    """
    try:
        rows = run_query(sql)

        if not rows:
            return "No data found."

        return "\n".join(
            str(tuple(row))
            for row in rows
        )

    except Exception as e:
        return f"Database error: {str(e)}"