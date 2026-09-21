from fastapi import FastAPI
from pydantic import BaseModel

from database import get_connection
from agent import ask_agent

app = FastAPI(title="AI Business Analytics API")
class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Business Analytics API is running"
    }


@app.get("/sales/summary")
def sales_summary():

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
        "total_revenue": result[1],
        "total_profit": result[2],
        "average_revenue": result[3]
    }

@app.get("/sales/revenue-by-region")
def revenue_by_region():

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
            "total_revenue": row[1]
        }
        for row in results
    ]
@app.get("/sales/profit-by-category")
def profit_by_category():

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
            "total_profit": row[1]
        }
        for row in results
    ]

@app.get("/sales/top-products")
def top_products():

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
            "total_revenue": row[1]
        }
        for row in results
    ]
@app.post("/ask")
def ask_business_question(request: QuestionRequest):

    answer = ask_agent(request.question)

    return {
        "question": request.question,
        "answer": answer
    }