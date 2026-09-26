#redis
from redis_cache import get_cached_answer, cache_answer
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from database import get_connection
from agent import ask_agent
from upload import read_csv_file, create_table_from_csv


app = FastAPI(title="AI Business Analytics API")
class QuestionRequest(BaseModel):
    question: str

app.mount("/dashboard", StaticFiles(directory="static", html=True), name="dashboard")

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
# @app.post("/ask")
# def ask_business_question(request: QuestionRequest):

#     answer = ask_agent(request.question)

#     return {
#         "question": request.question,
#         "answer": answer
#     }
#after using redis
@app.post("/ask")
def ask_business_question(request: QuestionRequest):

    # 1. Check Redis cache
    cached_answer = get_cached_answer(request.question)

    if cached_answer:
        return {
            "question": request.question,
            "answer": cached_answer,
            "source": "redis_cache"
        }

    # 2. Ask AI Agent
    answer = ask_agent(request.question)

    # 3. Store answer in Redis
    cache_answer(request.question, answer)

    return {
        "question": request.question,
        "answer": answer,
        "source": "ai_agent"
    }

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    try:
        df = read_csv_file(file.file)

        table_name = create_table_from_csv(
            df,
            file.filename
        )

        return {
            "message": "CSV uploaded and stored in PostgreSQL",
            "filename": file.filename,
            "table_name": table_name,
            "rows": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process CSV: {str(e)}"
        )
