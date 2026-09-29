# AI Business Analytics & Decision Support Agent

An AI-powered business analytics and decision-support platform that allows users to ask business questions in natural language and receive data-driven insights from structured business data.

The system combines **Python, FastAPI, PostgreSQL, LangChain, LangGraph, Groq LLMs, Redis, SQL, and Streamlit** to provide an intelligent natural-language business analytics experience.

---

## 🚀 Live Application

**Backend API:**

https://ai-business-analytics-agent.onrender.com

**Swagger API Documentation:**

https://ai-business-analytics-agent.onrender.com/docs

**FastAPI Dashboard:**

https://ai-business-analytics-agent.onrender.com/dashboard

**GitHub Repository:**

https://github.com/raoyashwani7/AI_Business_Analytics_Agent

---

# 📌 Project Overview

Traditional business analytics often requires users to write SQL queries or manually analyze dashboards.

This project provides a natural-language interface where users can ask questions such as:

* What is the total revenue?
* Which region generates the highest revenue?
* Which category has the highest profit?
* What are the top-selling products?
* Give me a business summary.
* Are there any unusual or anomalous sales?

The AI agent interprets the user's question, uses the available analytical tools, retrieves the required information from PostgreSQL, and generates a human-readable business response.

---

# 🎯 Project Objective

The main objective is to build a natural-language **Business Intelligence and AI Decision Support System** that combines:

* SQL-based data analysis
* Large Language Models
* Agentic AI
* LangChain
* LangGraph
* PostgreSQL
* Redis caching
* REST APIs
* Interactive data visualization

The goal is to make business analytics accessible through natural-language questions instead of requiring users to manually write SQL queries.

---

# ✨ Key Features

## 1. Natural Language Business Questions

Users can ask business questions in normal language.

Example:

```text
What is the total revenue?
```

```text
Which region has the highest revenue?
```

```text
Which category generates the highest profit?
```

```text
Are there any unusual or anomalous sales?
```

The AI agent processes the question and retrieves the relevant business information.

---

## 2. AI Business Analytics Agent

The project uses **LangGraph** to orchestrate the AI workflow.

The agent:

1. Receives the user's question.
2. Interprets the business request.
3. Determines the required database operation.
4. Uses the SQL database tool.
5. Retrieves relevant business data.
6. Analyzes the results.
7. Generates a concise business-oriented response.

---

## 3. PostgreSQL Database

The application uses PostgreSQL as the primary structured data source.

The main `sales` table contains **5,000 business transactions**.

Example fields include:

```text
order_id
order_date
customer_id
customer_name
product
category
region
quantity
unit_price
discount
revenue
cost
profit
payment_method
anomaly_flag
```

Verified dataset:

```text
Total records: 5,000
Total revenue: 166,378,556.00
Total profit: 41,364,626.00
```

---

## 4. Redis Caching

Redis is used to cache responses to repeated business questions.

For example, when the same question is asked repeatedly, the system can retrieve the cached response instead of unnecessarily repeating the complete processing flow.

The application also handles Redis connection failures gracefully.

---

## 5. FastAPI REST API

The backend is built using **FastAPI**.

### Available endpoints

| Method | Endpoint                    | Purpose                   |
| ------ | --------------------------- | ------------------------- |
| GET    | `/sales/summary`            | Overall sales summary     |
| GET    | `/sales/revenue-by-region`  | Revenue by region         |
| GET    | `/sales/profit-by-category` | Profit by category        |
| GET    | `/sales/top-products`       | Top-performing products   |
| GET    | `/datasets`                 | Available database tables |
| POST   | `/ask`                      | Ask a business question   |
| POST   | `/upload-csv`               | Upload business CSV data  |

Interactive API documentation is available through Swagger:

https://ai-business-analytics-agent.onrender.com/docs

---

# 🤖 AI Agent Workflow

```text
User Question
      ↓
FastAPI /ask
      ↓
LangGraph Agent
      ↓
Groq LLM
      ↓
SQL Database Tool
      ↓
PostgreSQL
      ↓
Business Data
      ↓
AI Analysis
      ↓
Business Insight
```
