import os
from typing import Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

from database import get_connection


load_dotenv()


# -----------------------------
# LLM
# -----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


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

tools = [
    get_sales_summary,
    get_revenue_by_region,
    get_profit_by_category,
    get_top_products
]


# Give tools to the LLM
llm_with_tools = llm.bind_tools(tools)


# -----------------------------
# LangGraph chatbot node
# -----------------------------

def chatbot(state: MessagesState):

    response = llm_with_tools.invoke(state["messages"])

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

    question = "Show me revenue by region"

    answer = ask_agent(question)

    print("\nAgent Answer:")
    print(answer)