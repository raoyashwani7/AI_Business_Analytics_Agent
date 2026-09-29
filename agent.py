import os
from typing import Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

from database import get_connection

from db_tools import query_database

load_dotenv()


# -----------------------------
# LLM
# -----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
SYSTEM_INSTRUCTION = """
You are an AI Business Analytics and Decision Support Agent.

For business questions:
1. Retrieve relevant business data using the available tools.
2. Analyze the results clearly.
3. State the key insight.
4. When appropriate, provide a practical business recommendation.
5. Never invent numerical values.
6. Base recommendations only on the available data and business knowledge.

Keep answers concise and easy for a manager to understand.
"""

# -----------------------------
# TOOL 1: Sales Summary
# -----------------------------

@tool
def get_sales_summary() -> dict:
    """Get total orders, total revenue, total profit and average revenue."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_orders,
            SUM(revenue) AS total_revenue,
            SUM(profit) AS total_profit,
            AVG(revenue) AS average_revenue
        FROM sales;
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "total_orders": result[0],
        "total_revenue": float(result[1]),
        "total_profit": float(result[2]),
        "average_revenue": float(result[3])
    }


# -----------------------------
# TOOL 2: Revenue by Region
# -----------------------------

@tool
def get_revenue_by_region() -> list[dict[str, Any]]:
    """Get total revenue for each region."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            region,
            SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "region": row[0],
            "total_revenue": float(row[1])
        }
        for row in results
    ]


# -----------------------------
# TOOL 3: Profit by Category
# -----------------------------

@tool
def get_profit_by_category() -> list[dict[str, Any]]:
    """Get total profit for each product category."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(profit) AS total_profit
        FROM sales
        GROUP BY category
        ORDER BY total_profit DESC;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "category": row[0],
            "total_profit": float(row[1])
        }
        for row in results
    ]


# -----------------------------
# TOOL 4: Top Products
# -----------------------------

@tool
def get_top_products() -> list[dict[str, Any]]:
    """Get the top 10 products by total revenue."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product,
            SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT 10;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "product": row[0],
            "total_revenue": float(row[1])
        }
        for row in results
    ]


# -----------------------------
# Register tools
# -----------------------------
@tool
def get_business_insights() -> list[dict[str, Any]]:
    """Analyze revenue and profit by region to support business decisions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            region,
            SUM(revenue) AS total_revenue,
            SUM(profit) AS total_profit
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "region": row[0],
            "total_revenue": float(row[1]),
            "total_profit": float(row[2])
        }
        for row in results
    ]
@tool
def get_monthly_sales_trend() -> list[dict[str, Any]]:
    """Get monthly revenue and profit trends."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATE_TRUNC('month', order_date) AS month,
            SUM(revenue) AS total_revenue,
            SUM(profit) AS total_profit
        FROM sales
        GROUP BY month
        ORDER BY month;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "month": str(row[0]),
            "total_revenue": float(row[1]),
            "total_profit": float(row[2])
        }
        for row in results
    ]

@tool
def get_sales_anomalies() -> list[dict[str, Any]]:
    """Find anomalous sales transactions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            order_id,
            order_date,
            customer_name,
            product,
            category,
            region,
            quantity,
            revenue,
            profit,
            anomaly_flag
        FROM sales
        WHERE anomaly_flag IS NOT NULL
          AND anomaly_flag <> ''
        ORDER BY revenue DESC;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "order_id": row[0],
            "order_date": str(row[1]),
            "customer_name": row[2],
            "product": row[3],
            "category": row[4],
            "region": row[5],
            "quantity": row[6],
            "revenue": float(row[7]),
            "profit": float(row[8]),
            "anomaly_flag": row[9]
        }
        for row in results
    ]

tools = [
    get_sales_summary,
    get_revenue_by_region,
    get_profit_by_category,
    get_top_products,
    get_business_insights,
    get_monthly_sales_trend,
    get_sales_anomalies,
    query_database
]

# Give tools to the LLM
llm_with_tools = llm.bind_tools(tools)


# -----------------------------
# LangGraph chatbot node
# -----------------------------

def chatbot(state: MessagesState):
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION}
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }
# -----------------------------
# Build LangGraph
# -----------------------------

builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")

builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

builder.add_edge("tools", "chatbot")


graph = builder.compile()


# -----------------------------
# Ask the business agent
# -----------------------------

def ask_agent(question: str):

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )

    return result["messages"][-1].content

if __name__ == "__main__":

    question = "Which category generated the highest revenue?"

    answer = ask_agent(question)

    print("\nAgent Answer:")
    print(answer)
